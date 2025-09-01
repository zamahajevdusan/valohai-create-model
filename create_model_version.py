import valohai
import json
import shutil

model_url = valohai.parameters("model_url").value

metadata = {
    "model.h5": {
        "factory": "eu-02",
        "valohai.tags": ["prod", "lemonade"],
        "valohai.model-versions": [model_url]
    },
}

# save all the models separately;
save_path = "/valohai/outputs/model.h5"
shutil.move("/valohai/inputs/model/model.h5", save_path)

metadata_path = "/valohai/outputs/valohai.metadata.jsonl"
with open(metadata_path, "w") as outfile:
    for file_name, file_metadata in metadata.items():
        json.dump({"file": file_name, "metadata": file_metadata}, outfile)
        outfile.write("\n")
