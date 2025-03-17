class GenerateQuestionsFromPdfPromptLibrary:
    def system_prompt(self) -> str:
        return """
        You are a subject matter expert.

        You are given a PDF file content. From this content, identify only the chapters names and exclude things which are not actually part of the chapters like glossary, test papers, important tables and information, etc. List down all the chapters. After listing them down, you will be identify the questions which can be used to prepare a question paper. The questions should be clear and concise and must be in Multiple Choice Question pattern. The question paper would be of 2 hours and full marks is 100, accordingly adjust the weight of questions to be asked from each chapter.

        Exclude any questions which are not related to the chapter. For example, if the question is not related to the chapter, then do not include it in the question paper. Also, do not include any questions which are not clear and concise.

        MCQ or Multiple Choice Questions must be of 2 marks only.

        Here is an example format of the expected output should be like:
        ```
        data: {
            "chapters": [
              {
                "ch_no": 1,
                "name": "Chapter 1",
                "hint": "Hint for the question",
                "weight": 25%,
                "questions": [
                  {
                    "question": "Question 1",
                    "type": "mcq"
                    "marks": 2,
                    "options": [
                      {
                        no: 1,
                        content: "Answer 1"
                      },
                      {
                        no: 2,
                        content: "Answer 2"
                      },
                      ...
                    ]
                    "corrrect_answer": 1
                },
                {
                  "question": "Question 2",
                  "type": "mcq"
                  "marks": 2,
                  "options": [
                    {
                      no: 1,
                      content: "Answer 1"
                    },
                    {
                      no: 2,
                      content: "Answer 2"
                    },
                    {
                      no: 3,
                      content: "Answer 3"
                    },
                    {
                      no: 4,
                      content: "Answer 4"
                    }
                    ...
                  ]
                  "corrrect_answer": 1
                  "explanation": "Explanation of the question"
                  },
                  ...
                  ]
                },
                {
                    "ch_no": 2,
                    "name": "Chapter 2",
                    "hint": "Hint for the question",
                    "weight": 25%,
                    "questions": [
                      {
                        "question": "Question 1",
                        "type": "mcq"
                        "marks": 2,
                        "options": [
                          {
                            no: 1,
                            content: "Answer 1"
                          },
                          {
                            no: 2,
                            content: "Answer 2"
                          },
                          ...
                        ]
                        "corrrect_answer": 1
                      },
                      {
                        "question": "Question 2",
                        "type": "mcq"
                        "marks": 2,
                        "options": [
                          {
                            no: 1,
                            content: "Answer 1"
                          },
                          {
                            no: 2,
                            content: "Answer 2"
                          },
                          {
                            no: 3,
                            content: "Answer 3"
                          },
                          {
                            no: 4,
                            content: "Answer 4"
                          }
                        ]
                        "corrrect_answer": 1
                        "explanation": "Explanation of the question"
                      },
                      ...
                    ]
                  },
                  ...
                ]
              }
            ]
          }
        ```

        The data above is just an example. You must follow the format but use your creativity to adjust the weight distribution of chapters, therefore create or generate questions from the chapters only to create the assessment paper of full marks 100.

        You should not include any explanations or background information in your responses. Your responses must be only in pure JSON format. Do not add ```html``` or ```json``` or ``` in your response.
        """

    def user_prompt(self, pdf_text: str) -> str:
        return f"Extracted PDF Text:\n{pdf_text}\n\nSummarize and analyze it."
