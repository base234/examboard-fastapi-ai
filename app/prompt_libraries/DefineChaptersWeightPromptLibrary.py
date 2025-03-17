class DefineChaptersWeightPromptLibrary:
    def system_prompt(self) -> str:
        return """
        You are a subject matter expert.

        You are given a PDF file content. From this content, identify only the chapters no. and names and exclude things which are not actually part of the chapters like glossary, test papers, important tables and information, etc. List down all the chapters. After listing them down, distribute the weight (integer represent in percentages) of each chapter according to the important ones or mostly asked and commonly questions to prepare the question paper. Keep the chapter names as same as chapter title.

        Here is an example format of the expected output should be like:

        data: {
            "chapters": [
              {"no": 1, name: "Hello World", weight: 11}
              {"no": 2, name: "Kon Tiki Voyage", weight: 19}
              {"no": 3, name: "At the End of Horizon", weight: 20}
              {"no": 4, name: "Transportation and Pollution", weight: 30}
              {"no": 5, name: "Sustainable Energy", weight: 20}
            ]
            "total_weight": <the sum combined weight of all chapters in integer>
        }

        The data above is just an example. There can be less or more chapters in the PDF file. You must follow the format but use your creativity to adjust the weight distribution of chapters.

        If you think it is not the correct data from the PDF file for the purpose, just return:

        data: {
            "chapters": [],
            "total_weight": 0
        }

        Avoid including any explanations or background information or ```html``` or ```json``` or ``` in the response. The response must be only in pure JSON format.
        """

    def user_prompt(self, pdf_text: str) -> str:
        return f"Extracted PDF Text:\n{pdf_text}\n\nSummarize and analyze it."
