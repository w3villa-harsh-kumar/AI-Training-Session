import json
import time
import os
from openai import OpenAI
import openai

# Ensure you've set your OpenAI API key in your environment variables
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

client = OpenAI()
def prepare_dataset():
    training_data = []
    for i in range(20):
        with open('training_data_' + str(i) + '.json', 'r') as f:
            data = json.load(f)
            print(data[0])
            training_data.append(data[0])
    
    with open('training_data.jsonl', 'w') as f:
        for entry in training_data:
            json.dump(entry, f)
            f.write('\n')

    print("Dataset prepared and saved as 'training_data.jsonl'")

def upload_training_file():
    with open('training_data.jsonl', 'rb') as file:
        training_file = client.files.create(
            file=file,
            purpose='fine-tune'
        )
    print(f"Training file uploaded with ID: {training_file.id}")
    return training_file.id

def create_fine_tuning_job(file_id):
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-4o-2024-08-06"
    )
    print(f"Fine-tuning job created with ID: {job.id}")
    return job.id

def check_job_status(job_id):
    job = client.fine_tuning.jobs.retrieve(job_id)
    return job.status

def monitor_fine_tuning_job(job_id):
    while True:
        status = check_job_status(job_id)
        print(f"Current status: {status}")
        if status == 'succeeded':
            print("Fine-tuning job completed successfully!", status)
            return job_id
        elif status == 'failed':
            print("Fine-tuning job failed.", status)
            return None
        time.sleep(60)  # Wait for 60 seconds before checking again

def get_fine_tuned_model_name(job_id):
    job = client.fine_tuning.jobs.retrieve(job_id)
    
    if job.status == "succeeded":
        model_name = job.fine_tuned_model
        print(f"Fine-tuned model name: {model_name}")
        return model_name
    else:
        print(f"The fine-tuning job has not succeeded. Current status: {job.status}")
        return None

def use_fine_tuned_model(model_name):
    response = openai.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are Brandon Farris, a famous youtuber, you need to answer in his style, tone and language."},
            {"role": "user", "content": "what do you for living"}
        ]
    )
    print("Response from fine-tuned model:")
    print(response.choices[0].message.content)

def main():
    print("step 1: preparing dataset")
    prepare_dataset()

    print("\nStep 2: Uploading training file")
    file_id = upload_training_file()

    print("\nStep 3: Creating and starting fine-tuning job")
    job_id = create_fine_tuning_job(file_id)

    print("\nStep 4: Monitoring fine-tuning job")
    completed_job_id = monitor_fine_tuning_job(job_id)

    if completed_job_id:
        print("\nStep 5: Retrieving fine-tuned model name")
        fine_tuned_model = get_fine_tuned_model_name(completed_job_id)

        if fine_tuned_model:
            print("\nStep 6: Using the fine-tuned model")
            use_fine_tuned_model(fine_tuned_model)
        else:
            print("Unable to use the fine-tuned model. Please check the job status and try again.")
    else:
        print("Fine-tuning job did not complete successfully. Unable to proceed.")

if __name__ == "__main__":
    main()