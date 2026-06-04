REQUIRED_SKILLS = ["Python","Azure","java"]

def evaluate_candidate(skills):
    normalize_skills = [skill.lower() for skill in skills]

    matched_skills = [skill for skill in REQUIRED_SKILLS
                      if skill.lower() in normalize_skills ]
    # por cada skill que se encuentre en required_skills, si tambien está en normalize skills, añadela a este array
    
    missing_skills = [skill for skill in REQUIRED_SKILLS
                        if not skill.lower() in normalize_skills]
    # por cada skill que se encuentre en required_skills, si no está en normalize skills, añadela a este array

    score = round(
        (len(matched_skills) / len(REQUIRED_SKILLS)) * 100
    )
    if score >= 70:
        decision =   "Possible candidate"
    elif score >= 40:
        decision = "Revision"
    else:
        decision =  "Rejected"

    return {
        "decision" : decision,
        "score" : score,
        "matched_skills" : matched_skills,
        "missing_skills" : missing_skills
    }

        

 