import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models import Opportunity, VolunteerProfile, LearningResource, suggest_learning_path


def test_suggest_learning_path():
    vol = VolunteerProfile(id=1, name="Alice", desired_skills=["python", "design"])
    opps = [
        Opportunity(id=1, title="Python Mentor", skills_required=["Python", "teaching"]),
        Opportunity(id=2, title="Graphic Design", skills_required=["design"]),
        Opportunity(id=3, title="Marketing", skills_required=["seo"]),
    ]
    resources = [
        LearningResource(skill="python", url="https://example.com/python-course"),
        LearningResource(skill="design", url="https://example.com/design-guide"),
        LearningResource(skill="cooking", url="https://example.com/cooking"),
    ]

    result = suggest_learning_path(vol, opps, resources)
    assert "Python Mentor" in result["opportunities"]
    assert "Graphic Design" in result["opportunities"]
    assert "Marketing" not in result["opportunities"]
    assert "https://example.com/python-course" in result["resources"]
    assert "https://example.com/design-guide" in result["resources"]
    assert "https://example.com/cooking" not in result["resources"]
