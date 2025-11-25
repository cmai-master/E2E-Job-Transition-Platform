"""
Resume Parser Service
Extracts information from resume files (PDF, DOCX)
"""

import re
from typing import Optional, List, Dict, Any
from datetime import datetime
import io


class ResumeParser:
    """Resume parser service for extracting information from resume files"""

    # Common section headers
    SECTION_HEADERS = {
        "experience": [
            "experience", "work experience", "employment", "work history",
            "professional experience", "경력", "경력사항", "직무경력"
        ],
        "education": [
            "education", "academic", "학력", "학력사항"
        ],
        "skills": [
            "skills", "technical skills", "technologies", "기술", "스킬", "보유기술"
        ],
        "summary": [
            "summary", "objective", "about", "profile", "자기소개", "요약"
        ],
        "projects": [
            "projects", "프로젝트", "프로젝트 경험"
        ],
        "certifications": [
            "certifications", "certificates", "자격증", "자격사항"
        ],
    }

    # Email pattern
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Phone patterns (international and Korean)
    PHONE_PATTERNS = [
        r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US format
        r'010[-.\s]?[0-9]{4}[-.\s]?[0-9]{4}',  # Korean mobile
        r'\+82[-.\s]?10[-.\s]?[0-9]{4}[-.\s]?[0-9]{4}',  # Korean international
    ]

    # URL patterns
    URL_PATTERNS = {
        "linkedin": r'linkedin\.com/in/[\w-]+',
        "github": r'github\.com/[\w-]+',
        "portfolio": r'https?://(?:www\.)?[\w.-]+\.[a-zA-Z]{2,}(?:/[\w.-]*)*',
    }

    def __init__(self):
        """Initialize the resume parser"""
        self._pdf_parser = None
        self._docx_parser = None

    async def parse_pdf(self, content: bytes) -> Dict[str, Any]:
        """
        Parse PDF resume file

        Args:
            content: PDF file content as bytes

        Returns:
            Dictionary with extracted information
        """
        try:
            import PyPDF2
            from io import BytesIO

            pdf_reader = PyPDF2.PdfReader(BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return await self._extract_info(text)
        except ImportError:
            return {"error": "PyPDF2 not installed", "raw_text": ""}
        except Exception as e:
            return {"error": str(e), "raw_text": ""}

    async def parse_docx(self, content: bytes) -> Dict[str, Any]:
        """
        Parse DOCX resume file

        Args:
            content: DOCX file content as bytes

        Returns:
            Dictionary with extracted information
        """
        try:
            from docx import Document
            from io import BytesIO

            doc = Document(BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs])

            return await self._extract_info(text)
        except ImportError:
            return {"error": "python-docx not installed", "raw_text": ""}
        except Exception as e:
            return {"error": str(e), "raw_text": ""}

    async def _extract_info(self, text: str) -> Dict[str, Any]:
        """
        Extract information from resume text

        Args:
            text: Raw resume text

        Returns:
            Dictionary with extracted information
        """
        result = {
            "raw_text": text,
            "contact": self._extract_contact(text),
            "skills": self._extract_skills(text),
            "sections": self._identify_sections(text),
        }

        return result

    def _extract_contact(self, text: str) -> Dict[str, Optional[str]]:
        """Extract contact information"""
        contact = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None,
        }

        # Extract email
        email_match = re.search(self.EMAIL_PATTERN, text)
        if email_match:
            contact["email"] = email_match.group()

        # Extract phone
        for pattern in self.PHONE_PATTERNS:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact["phone"] = phone_match.group()
                break

        # Extract URLs
        for key, pattern in self.URL_PATTERNS.items():
            if key in ["linkedin", "github"]:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    contact[key] = f"https://{match.group()}"

        return contact

    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from resume text

        This is a basic extraction that looks for common technical skills.
        For production, this should be enhanced with NER or LLM.
        """
        # Common technical skills to look for
        common_skills = [
            # Programming Languages
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
            "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
            # Frontend
            "React", "Vue", "Angular", "Next.js", "Nuxt", "Svelte", "HTML", "CSS",
            "Sass", "LESS", "Tailwind", "Bootstrap", "jQuery",
            # Backend
            "Node.js", "Express", "FastAPI", "Django", "Flask", "Spring", "Rails",
            "ASP.NET", "GraphQL", "REST",
            # Databases
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Neo4j",
            "SQLite", "Oracle", "SQL Server", "DynamoDB", "Cassandra",
            # Cloud & DevOps
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
            "Jenkins", "GitHub Actions", "CircleCI", "GitLab CI",
            # AI/ML
            "TensorFlow", "PyTorch", "Keras", "scikit-learn", "pandas", "NumPy",
            "OpenAI", "LangChain", "Hugging Face",
            # Tools
            "Git", "Linux", "Bash", "Vim", "VS Code", "IntelliJ", "Jira", "Confluence",
        ]

        text_lower = text.lower()
        found_skills = []

        for skill in common_skills:
            # Check for skill with word boundaries
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return found_skills

    def _identify_sections(self, text: str) -> Dict[str, str]:
        """
        Identify and extract resume sections

        Args:
            text: Resume text

        Returns:
            Dictionary mapping section names to their content
        """
        sections = {}
        lines = text.split('\n')
        current_section = "header"
        section_content = []

        for line in lines:
            line_lower = line.lower().strip()

            # Check if this line is a section header
            found_section = None
            for section_name, headers in self.SECTION_HEADERS.items():
                for header in headers:
                    if line_lower == header or line_lower.startswith(header + ":"):
                        found_section = section_name
                        break
                if found_section:
                    break

            if found_section:
                # Save previous section
                if section_content:
                    sections[current_section] = '\n'.join(section_content).strip()
                current_section = found_section
                section_content = []
            else:
                section_content.append(line)

        # Save last section
        if section_content:
            sections[current_section] = '\n'.join(section_content).strip()

        return sections

    async def parse_with_llm(self, text: str, llm_client=None) -> Dict[str, Any]:
        """
        Parse resume using LLM for better extraction

        Args:
            text: Resume text
            llm_client: Optional LLM client (OpenAI, Anthropic, etc.)

        Returns:
            Structured resume data
        """
        # This is a placeholder for LLM-based parsing
        # In production, this would use GPT-4 or Claude to extract structured data

        prompt = f"""
        Extract the following information from this resume in JSON format:
        - full_name: string
        - email: string
        - phone: string
        - linkedin_url: string
        - github_url: string
        - summary: string (brief professional summary)
        - skills: list of strings (technical skills)
        - experience: list of objects with (company, title, start_date, end_date, description)
        - education: list of objects with (institution, degree, field, graduation_date)

        Resume:
        {text[:4000]}  # Truncate for token limits

        Return only valid JSON.
        """

        # For now, return basic extraction
        return await self._extract_info(text)
