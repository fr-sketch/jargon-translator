# train_t5.py
from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, DataCollatorForSeq2Seq
from transformers import Trainer, TrainingArguments


MODELS = {
    "ai-forever/ruT5-base": "./models/ai-forever-ruT5-base",
    "cointegrated/rut5-base": "./models/cointegrated-rut5-base",
    "cointegrated/rut5-small": "./models/cointegrated-rut5-small",
}

def load_slang_dataset(train_path="train.csv", valid_path="valid.csv"):
    data_files = {
        "train": train_path,
        "validation": valid_path,
    }
    dataset = load_dataset("csv", data_files=data_files)
    return dataset

def train_one_model(hf_model_name: str, output_dir: str):
    dataset = load_slang_dataset()
    tokenizer = T5Tokenizer.from_pretrained(hf_model_name)
    model = T5ForConditionalGeneration.from_pretrained(hf_model_name)

    max_input_length = 128
    max_target_length = 128

    def preprocess_function(examples):
        # Добавляем домен и префикс задачи для T5
        inputs = [
            f"domain: {d} | translate slang to formal: {text}"
            for d, text in zip(examples["domain"], examples["source_text"])
        ]
        targets = examples["target_text"]

        model_inputs = tokenizer(
            inputs,
            max_length=max_input_length,
            truncation=True,
        )

        labels = tokenizer(
            targets,
            max_length=max_target_length,
            truncation=True,
        )

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = dataset.map(preprocess_function, batched=True)
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    training_args = TrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=3e-4,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        save_total_limit=2,
        report_to=["none"],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

if __name__ == "__main__":
    for hf_name, out_dir in MODELS.items():
        print(f"=== Training {hf_name} -> {out_dir} ===")
        train_one_model(hf_name, out_dir)
