import os
import openai
import re

from . import constants

from .logger import get_logger


class Core:
    def __init__(self, debug, output, model=constants.DEFAULT_MODEL):
        self.logger = get_logger(debug)
        self.output = output
        self.model = model
        self.prompt_template = '''
            あなたは優秀なエンジニアです。
            以下のコードのテストコードを実装してください。

            ```{code}```

            ただしテストコードのみを返答してください。
            テストコードの説明は不要です。
        '''

    def generate_test_code(self, path):
        code = None
        with open(path, 'r') as f:
            code = f.read()

        filename = f"test_{os.path.basename(path)}"
        output_path = f"{self.output}/{filename}"
        if 'def ' in code:
            prompt = self.prompt_template.format(
                code=code,
            )
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            content = response["choices"][0]["message"]["content"]
            self.logger.info(f"content => {content}")
            m = re.search("```python?(.*)\n```", content, flags=re.DOTALL)
            test_code = m.group().replace("```python", "").replace("```", "")

            # create file
            self.logger.info(f"output_path => {output_path}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as file:
                file.write(test_code)
        else:
            self.logger.info(f"skip file => {output_path}")
