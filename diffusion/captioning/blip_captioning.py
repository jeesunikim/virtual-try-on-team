#  Adapted from https://github.com/bmaltais/kohya_ss/tree/17f58c8bb9bc38773a870df58e1ae788abf6753b


# export PYTHONPATH="/workspace/edeyneka/2023_11_05_finetuning_style/kohya_ss:$PYTHONPATH"
# export PYTHONPATH="/workspace/edeyneka/2023_11_05_finetuning_style/kohya_ss/finetune:$PYTHONPATH"
import subprocess
import os
from library.common_gui import get_folder_path, add_pre_postfix
from library.custom_logging import setup_logging
import argparse
import sys

# Set up logging
log = setup_logging()

PYTHON = 'python3' if os.name == 'posix' else './venv/Scripts/python.exe'


def caption_images(
    train_data_dir,
    caption_file_ext,
    batch_size,
    num_beams,
    top_p,
    max_length,
    min_length,
    beam_search,
    prefix,
    postfix,
):
    # Check if the image folder is provided
    if train_data_dir == '':
        msgbox('Image folder is missing...')
        return

    # Check if the caption file extension is provided
    if caption_file_ext == '':
        msgbox('Please provide an extension for the caption files.')
        return

    log.info(f'Captioning files in {train_data_dir}...')

    # Construct the command to run
        # Construct the command to run
    run_cmd = f'{PYTHON} "make_captions.py"'
    run_cmd += f' --batch_size="{int(batch_size)}"'
    run_cmd += f' --num_beams="{int(num_beams)}"'
    run_cmd += f' --top_p="{top_p}"'
    run_cmd += f' --max_length="{int(max_length)}"'
    run_cmd += f' --min_length="{int(min_length)}"'
    if beam_search:
        run_cmd += f' --beam_search'
    if caption_file_ext != '':
        run_cmd += f' --caption_extension="{caption_file_ext}"'
    run_cmd += f' "{train_data_dir}"'
    run_cmd += f' --caption_weights="https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth"'

    log.info(run_cmd)
    print(run_cmd)

    # Run the command
    if os.name == 'posix':
        os.system(run_cmd)
    else:
        subprocess.run(run_cmd)

    # Add prefix and postfix
    add_pre_postfix(
        folder=train_data_dir,
        caption_file_ext=caption_file_ext,
        prefix=prefix,
        postfix=postfix,
    )

    log.info('...captioning done')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='BLIP Captioning')
    parser.add_argument('--train_data_dir', type=str, required=True)
    parser.add_argument('--caption_file_ext', type=str, default='.txt')
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--num_beams', type=int, default=1)
    parser.add_argument('--top_p', type=float, default=0.9)
    parser.add_argument('--max_length', type=float, default=75)
    parser.add_argument('--min_length', type=float, default=5)
    parser.add_argument('--beam_search', action="store_true")
    parser.add_argument('--prefix', type=str, default='')
    parser.add_argument('--postfix', type=str, default='')

    args = parser.parse_args()

    caption_images(
        train_data_dir=args.train_data_dir,
        caption_file_ext=args.caption_file_ext,
        batch_size=args.batch_size,
        num_beams=args.num_beams,
        top_p=args.top_p,
        max_length=args.max_length,
        min_length=args.min_length,
        beam_search=args.beam_search,
        prefix=args.prefix,
        postfix=args.postfix,
        )