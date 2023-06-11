import people_also_ask


class GoogleScrape:
    def __init__(self):
        pass

    def scrape(self, search_term=None):
        questions = people_also_ask.get_related_questions(f"About {search_term}")
        result = ""
        for each in questions:
            answer = people_also_ask.get_answer(each)
            response = answer.get("response", None)
            result += response + "\n\n"

        return result
