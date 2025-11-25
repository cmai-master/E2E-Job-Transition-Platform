"use client"

import { useEffect, useState } from "react"
import { useAuthStore } from "@/store/auth"
import { userApi } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { Skill, CareerHistory, Education } from "@/types/auth"

export default function ProfilePage() {
  const { user, profile, fetchProfile, updateProfile, isLoading } = useAuthStore()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    full_name: "",
    phone: "",
    bio: "",
    linkedin_url: "",
    github_url: "",
    portfolio_url: "",
  })
  const [newSkill, setNewSkill] = useState("")
  const [skills, setSkills] = useState<Skill[]>([])
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved" | "error">("idle")

  useEffect(() => {
    fetchProfile()
  }, [fetchProfile])

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || "",
        phone: user.phone || "",
        bio: user.bio || "",
        linkedin_url: user.linkedin_url || "",
        github_url: user.github_url || "",
        portfolio_url: user.portfolio_url || "",
      })
    }
    if (profile) {
      setSkills(profile.skills || [])
    }
  }, [user, profile])

  const handleSave = async () => {
    setSaveStatus("saving")
    try {
      await updateProfile(formData)
      setIsEditing(false)
      setSaveStatus("saved")
      setTimeout(() => setSaveStatus("idle"), 2000)
    } catch (error) {
      setSaveStatus("error")
      setTimeout(() => setSaveStatus("idle"), 2000)
    }
  }

  const handleAddSkill = async () => {
    if (!newSkill.trim()) return

    try {
      const skill = await userApi.addSkill({
        skill_name: newSkill.trim(),
        category: "technical",
        proficiency_level: 3,
        years_used: null,
      })
      setSkills([...skills, skill])
      setNewSkill("")
    } catch (error) {
      console.error("Failed to add skill:", error)
    }
  }

  const handleDeleteSkill = async (skillId: string) => {
    try {
      await userApi.deleteSkill(skillId)
      setSkills(skills.filter(s => s.id !== skillId))
    } catch (error) {
      console.error("Failed to delete skill:", error)
    }
  }

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      await userApi.uploadResume(file)
      fetchProfile()
    } catch (error) {
      console.error("Failed to upload resume:", error)
    }
  }

  if (isLoading && !user) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
        {!isEditing ? (
          <Button onClick={() => setIsEditing(true)}>Edit Profile</Button>
        ) : (
          <div className="space-x-2">
            <Button variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
            <Button onClick={handleSave} disabled={saveStatus === "saving"}>
              {saveStatus === "saving" ? "Saving..." : "Save Changes"}
            </Button>
          </div>
        )}
      </div>

      {saveStatus === "saved" && (
        <div className="p-3 bg-green-50 text-green-700 rounded-md">
          Profile saved successfully!
        </div>
      )}

      {saveStatus === "error" && (
        <div className="p-3 bg-red-50 text-red-700 rounded-md">
          Failed to save profile. Please try again.
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Basic Info */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>Your personal details and contact information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    value={user?.email || ""}
                    disabled
                    className="bg-gray-50"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="full_name">Full Name</Label>
                  <Input
                    id="full_name"
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                    disabled={!isEditing}
                    className={!isEditing ? "bg-gray-50" : ""}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    disabled={!isEditing}
                    className={!isEditing ? "bg-gray-50" : ""}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <textarea
                  id="bio"
                  value={formData.bio}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  disabled={!isEditing}
                  className={`w-full min-h-[100px] rounded-md border border-input px-3 py-2 text-sm ${!isEditing ? "bg-gray-50" : ""}`}
                  placeholder="Tell us about yourself..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="linkedin_url">LinkedIn URL</Label>
                  <Input
                    id="linkedin_url"
                    value={formData.linkedin_url}
                    onChange={(e) => setFormData({ ...formData, linkedin_url: e.target.value })}
                    disabled={!isEditing}
                    className={!isEditing ? "bg-gray-50" : ""}
                    placeholder="https://linkedin.com/in/..."
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="github_url">GitHub URL</Label>
                  <Input
                    id="github_url"
                    value={formData.github_url}
                    onChange={(e) => setFormData({ ...formData, github_url: e.target.value })}
                    disabled={!isEditing}
                    className={!isEditing ? "bg-gray-50" : ""}
                    placeholder="https://github.com/..."
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="portfolio_url">Portfolio URL</Label>
                  <Input
                    id="portfolio_url"
                    value={formData.portfolio_url}
                    onChange={(e) => setFormData({ ...formData, portfolio_url: e.target.value })}
                    disabled={!isEditing}
                    className={!isEditing ? "bg-gray-50" : ""}
                    placeholder="https://..."
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Resume Upload */}
        <div>
          <Card>
            <CardHeader>
              <CardTitle>Resume</CardTitle>
              <CardDescription>Upload your resume for AI analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {user?.resume_url ? (
                  <div className="p-4 bg-green-50 rounded-md">
                    <p className="text-sm text-green-700">Resume uploaded</p>
                    <a
                      href={user.resume_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline"
                    >
                      View Resume
                    </a>
                  </div>
                ) : (
                  <div className="p-4 bg-gray-50 rounded-md text-center">
                    <p className="text-sm text-gray-600 mb-2">No resume uploaded</p>
                  </div>
                )}
                <div>
                  <Label htmlFor="resume" className="cursor-pointer">
                    <div className="border-2 border-dashed border-gray-300 rounded-md p-4 text-center hover:border-blue-500 transition-colors">
                      <p className="text-sm text-gray-600">
                        Click to upload PDF or DOCX
                      </p>
                    </div>
                  </Label>
                  <Input
                    id="resume"
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleResumeUpload}
                    className="hidden"
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Skills Section */}
      <Card>
        <CardHeader>
          <CardTitle>Skills</CardTitle>
          <CardDescription>Add your technical and professional skills</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="Add a skill (e.g., Python, React, Project Management)"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleAddSkill()}
              />
              <Button onClick={handleAddSkill}>Add</Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {skills.map((skill) => (
                <span
                  key={skill.id}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
                >
                  {skill.skill_name}
                  <button
                    onClick={() => handleDeleteSkill(skill.id)}
                    className="ml-2 text-blue-600 hover:text-blue-800"
                  >
                    &times;
                  </button>
                </span>
              ))}
              {skills.length === 0 && (
                <p className="text-sm text-gray-500">No skills added yet</p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Career History */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Career History</CardTitle>
            <CardDescription>Your work experience</CardDescription>
          </div>
          <Button variant="outline" size="sm">Add Experience</Button>
        </CardHeader>
        <CardContent>
          {profile?.career_history && profile.career_history.length > 0 ? (
            <div className="space-y-4">
              {profile.career_history.map((career: CareerHistory) => (
                <div key={career.id} className="border-b pb-4 last:border-0">
                  <h4 className="font-medium">{career.title}</h4>
                  <p className="text-sm text-gray-600">{career.company_name}</p>
                  <p className="text-xs text-gray-500">
                    {new Date(career.start_date).toLocaleDateString()} -
                    {career.is_current ? " Present" : career.end_date ? ` ${new Date(career.end_date).toLocaleDateString()}` : ""}
                  </p>
                  {career.description && (
                    <p className="mt-2 text-sm text-gray-700">{career.description}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No work experience added yet</p>
          )}
        </CardContent>
      </Card>

      {/* Education */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Education</CardTitle>
            <CardDescription>Your educational background</CardDescription>
          </div>
          <Button variant="outline" size="sm">Add Education</Button>
        </CardHeader>
        <CardContent>
          {profile?.education && profile.education.length > 0 ? (
            <div className="space-y-4">
              {profile.education.map((edu: Education) => (
                <div key={edu.id} className="border-b pb-4 last:border-0">
                  <h4 className="font-medium">{edu.degree || "Degree"}</h4>
                  <p className="text-sm text-gray-600">{edu.institution}</p>
                  {edu.field_of_study && (
                    <p className="text-sm text-gray-500">{edu.field_of_study}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No education added yet</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
