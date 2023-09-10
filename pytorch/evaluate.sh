python ./uie_pytorch/evaluate.py \
    --model_path ./checkpoint/model-best-4000-torch \
    --test_path ./data/dev.txt \
    --batch_size 16 \
    --max_seq_len 512