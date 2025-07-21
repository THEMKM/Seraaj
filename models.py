from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Opportunity:
    id: int
    title: str
    skills_required: List[str]

@dataclass
class LearningResource:
    skill: str
    url: str

@dataclass
class VolunteerProfile:
    id: int
    name: str
    desired_skills: List[str] = field(default_factory=list)
    completed_opportunities: List[int] = field(default_factory=list)


def suggest_learning_path(
    volunteer: VolunteerProfile,
    opportunities: List[Opportunity],
    resources: List[LearningResource],
) -> Dict[str, List[str]]:
    """Return opportunity titles and resource URLs matching desired skills."""
    opp_matches = []
    res_matches = []
    desired_set = set(map(str.lower, volunteer.desired_skills))

    for opp in opportunities:
        if desired_set.intersection(map(str.lower, opp.skills_required)):
            if opp.id not in volunteer.completed_opportunities:
                opp_matches.append(opp.title)

    for res in resources:
        if res.skill.lower() in desired_set:
            res_matches.append(res.url)

    return {"opportunities": opp_matches, "resources": res_matches}
