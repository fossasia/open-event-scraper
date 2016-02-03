# result is a dictionary of the excel sheet
def get_linkedin_url(result):
    if result.has_key("linkedin"):
        return result["linkedin"]
    elif result.has_key("Linkedin"):
        return result["Linkedin"]
    elif result.has_key("LinkedIn"):
        return result["LinkedIn"]
    elif result.has_key("linkedIn"):
        return result["linkedIn"]
    return ""


def get_pic_url(result):
    if result.has_key("Photo for Website and Program"):
        return result["Photo for Website and Program"]
    elif result.has_key("image"):
        return result["image"]
    return ""
