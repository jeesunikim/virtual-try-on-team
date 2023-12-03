cd /workspace/edeyneka/2023_11_05_finetuning_style/kohya_ss
apt install python3.10-venv
apt update -y
apt install -y python3-tk
python3 -m pip install -r /workspace/edeyneka/2023_11_05_finetuning_style/stable-diffusion-webui/requirements.txt
accelerate launch --num_cpu_threads_per_process=2 "./train_network.py" --enable_bucket \
    --min_bucket_reso=256 --max_bucket_reso=2048 --pretrained_model_name_or_path="/workspace/edeyneka/2023_11_05_finetuning_style/experiments/experiment_myphotos/model/katedeyneka-000005.safetensors" \
    --train_data_dir="/workspace/edeyneka/2023_11_05_finetuning_style/experiments/experiment_clothes/img" \
    --resolution="512,768" \
    --output_dir="/workspace/edeyneka/2023_12_03_hackathon/kate-deyneka/playground/experiment_clothes/model" \
    --logging_dir="/workspace/edeyneka/2023_12_03_hackathon/kate-deyneka/playground/experiment_clothes/log" --network_alpha="1" \
    --save_model_as=safetensors --network_module=networks.lora --text_encoder_lr=5e-05 --unet_lr=0.0001 --network_dim=8 \
    --output_name="xyzblackdress_katedeyneka" --lr_scheduler_num_cycles="8" --no_half_vae --learning_rate="0.0001" \
    --lr_scheduler="cosine" --lr_warmup_steps="104" --train_batch_size="1" --max_train_steps="1040" --save_every_n_epochs="1" \
    --mixed_precision="fp16" --save_precision="fp16" --cache_latents --optimizer_type="AdamW8bit" --max_data_loader_n_workers="0" \
    --bucket_reso_steps=64 --xformers --bucket_no_upscale --noise_offset=0.0 --sample_sampler=euler_a \
    --sample_prompts="/workspace/edeyneka/2023_12_03_hackathon/kate-deyneka/playground/experiment_clothes/model/sample/prompt.txt" \
    --sample_every_n_epochs="1"