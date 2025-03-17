class ShortBlogPostPromptLibrary:
    def system_prompt(self) -> str:
        return """
        Provide response strictly in the provided HTML format. Do not explain what you are doing or include any non-HTML content. Just reply with the blog post in the mentioned HTML format.

        <h2>Short Blog Post</h2>
        <h3>1. Introduction</h3>
        <p>This is a short blog post about {topic}. It will be published on the website {website}. The blog post will be about {keywords}.</p>
        <h3>2. Content</h3>
        <p>The blog post will be written in a conversational tone and will include the following sections:</p>
        """

    def user_prompt(
        self,
        topic: str,
        keywords: str,
    ) -> str:
        return f"""

            Important: Do NOT include code block formatting such as ` ```html ` or ` ``` ` in your response. Only return the html content as plain text.

            Below I am sharing Q&A. Please refer to it for more information, it will help you to generate a description for the campaign.
            Q&As:

        """
