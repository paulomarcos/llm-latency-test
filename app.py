import time
from typing import List

from src.llms import LLM
from src import utils


def run_test(models: List[LLM], data: List[dict], store_csv: bool):

    result_data = []

    for row in data:
        prompt = row.get('prompt')
        for model in models:
            model.current_latency, model.answer = model.record_latency(prompt=prompt)
            print(f"{model.model_name}: ({model.current_latency}) {model.answer}")

            # Sleep for five seconds to avoid over-calling the API
            time.sleep(2)

        csv_columns = {}
        for model in models:
            csv_columns[f"{model.model_name} latency"] = model.current_latency
            csv_columns[f"{model.model_name} answer"] = model.answer
            csv_columns[f"{model.model_name} length"] = len(model.answer)

        # Append data to store it as .csv later on
        if store_csv:
            csv_columns['input prompt'] = prompt
            csv_columns['input length'] = len(prompt)
            result_data.append(csv_columns)

    if store_csv:
        utils.save_result_as_csv(result_data, file_name="../gemini_flash_result.csv")


if __name__ == "__main__":

    models = [LLM(model="gemini-pro"), LLM(model='gemini-flash'), LLM(model="gpt-3"), LLM(model="gpt-4")]

    # models = [LLM(model='gemini-flash')]

    data = utils.load_data(file_name="data.json")

    run_test(models=models, data=data, store_csv=True)
