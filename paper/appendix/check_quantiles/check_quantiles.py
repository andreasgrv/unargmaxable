import os
import tqdm
import torch
import numpy as np
import matplotlib.pyplot as plt

from transformers import pipeline
from argparse import ArgumentParser


def get_device_int(device):
    if device == 'cpu':
        return -1
    else:
        return 0


def get_activation(model, source_sents, target_sents, device):

    source_tokens = model.tokenizer(source_sents, truncation=True, padding=True, return_tensors='pt')
    src_input_ids = source_tokens['input_ids'].to(device)
    src_attention_mask = source_tokens['attention_mask'].to(device)

    with model.tokenizer.as_target_tokenizer():
        target_tokens = model.tokenizer(target_sents, truncation=True, padding=True, return_tensors='pt')

    trg_input_ids = target_tokens['input_ids'].to(device)
    trg_attention_mask = target_tokens['attention_mask'].to(device)

    with torch.no_grad():
        r = model.model.forward(input_ids=src_input_ids,
                                attention_mask=src_attention_mask,
                                decoder_input_ids=trg_input_ids,
                                decoder_attention_mask=trg_attention_mask,
                                output_hidden_states=True,
                                # Below is needed for WMT models to return all activations
                                use_cache=False)
    pre_image = r.decoder_hidden_states[-1].cpu().detach().numpy()

    return pre_image



if __name__ == "__main__":

    parser = ArgumentParser(description='Check range of activations in a neural network.')
    parser.add_argument('--data', type=str, required=True, help='Path to train files.')
    parser.add_argument('--model', type=str, required=True, help='Name of huggingface model')
    parser.add_argument('--num-lines', type=int, required=True, help='Number of lines to process.')
    parser.add_argument('--device', type=str, default='cpu', help='Device to run on.')

    args = parser.parse_args()

    SOURCE_FILE = 'train.src'
    TARGET_FILE = 'train.trg'

    BATCH_SIZE = 16

    source_path = os.path.join(args.data, SOURCE_FILE)
    target_path = os.path.join(args.data, TARGET_FILE)

    device = torch.device(args.device)

    print('Loading model %s...' % args.model)
    model = pipeline('text2text-generation', args.model, device=get_device_int(args.device))

    num_lines = 0
    mins = []
    maxs = []
    print('Processing %d lines...' % args.num_lines)
    pbar = tqdm.tqdm(total=args.num_lines)
    with open(source_path, 'r') as src, open(target_path, 'r') as trg:
        src_sents, trg_sents = [], []
        for src_sent, trg_sent in zip(src, trg):
            src_sent = src_sent.strip()
            trg_sent = trg_sent.strip()

            num_lines += 1
            pbar.update(1)

            if len(src_sent) < 1 or len(trg_sent) < 1:
                continue

            if num_lines == args.num_lines:
                break

            src_sents.append(src_sent)
            trg_sents.append(trg_sent)

            if len(src_sents) == BATCH_SIZE:
                try:
                    act = get_activation(model, src_sents, trg_sents, device=device)
                except (ValueError, RuntimeError) as e:
                    print(e)
                    continue
                finally:
                    src_sents = []
                    trg_sents = []
                mins.append(act.min(axis=2).ravel())
                maxs.append(act.max(axis=2).ravel())
    pbar.close()

    mins = np.hstack(mins)
    maxs = np.hstack(maxs)

    # print(all_preimages.shape)
    # print('Megabytes used: %.2f' % (all_preimages.nbytes / 1e6))

    LOWER_PRCNTL = .005
    UPPER_PRCNTL = 1 - LOWER_PRCNTL
    lower_min = np.quantile(mins, LOWER_PRCNTL)
    upper_min = np.quantile(mins, UPPER_PRCNTL)

    lower_max = np.quantile(maxs, LOWER_PRCNTL)
    upper_max = np.quantile(maxs, UPPER_PRCNTL)

    print('Min values range [%.2f, %.2f]' % (lower_min, upper_min))
    print('Max values range [%.2f, %.2f]' % (lower_max, upper_max))

    min_overall = mins.min()
    max_overall = maxs.max()
    print('Minimum overall: %f' % min_overall)
    print('Maximum overall: %f' % max_overall)
