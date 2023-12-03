cd /workspace/edeyneka/2023_11_05_finetuning_style/kohya_ss
apt install python3.10-venv
apt update -y
apt install -y python3-tk
python3 -m pip install -r /workspace/edeyneka/2023_11_05_finetuning_style/stable-diffusion-webui/requirements.txt
accelerate launch --num_cpu_threads_per_process=2 "./train_db.py" --enable_bucket \
    --min_bucket_reso=256 --max_bucket_reso=2048 \
    --pretrained_model_name_or_path="/workspace/edeyneka/2023_11_05_finetuning_style/stable-diffusion-webui/models/Stable-diffusion/realisticVisionV51_v51VAE.safetensors" \
    --train_data_dir="/workspace/edeyneka/2023_11_05_finetuning_style/experiments/experiment_myphotos/img" --resolution="512,768" \
    --output_dir="/workspace/edeyneka/2023_12_03_hackathon/kate-deyneka/playground/experiment_identity/model" \
    --logging_dir="/workspace/edeyneka/2023_12_03_hackathon/kate-deyneka/playground/experiment_identity/log" \
    --save_model_as=safetensors --output_name="katedeyneka" --lr_scheduler_num_cycles="8" --max_data_loader_n_workers="0" \
    --learning_rate="1e-05" --lr_scheduler="cosine" --lr_warmup_steps="88" --train_batch_size="1" --max_train_steps="880" \
    --save_every_n_epochs="1" --mixed_precision="bf16" --save_precision="bf16" --cache_latents --optimizer_type="AdamW8bit" \
    --max_data_loader_n_workers="0" --bucket_reso_steps=64 --xformers --bucket_no_upscale --noise_offset=0.0 \
    --sample_sampler=euler_a \
    --sample_prompts="/workspace/edeyneka/2023_12_03_hackathon/kate-deyneka/playground/experiment_identity/model/sample/prompt.txt" \
    --sample_every_n_epochs="1"