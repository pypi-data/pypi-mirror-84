import logging
from typing import Any, Optional, Text, Union

from tokenizers import AddedToken, pre_tokenizers, processors
from tokenizers.normalizers import Lowercase, Sequence
from transformers import RobertaTokenizerFast

Token = Union[Text, AddedToken]

logger = logging.getLogger(__name__)


VOCAB_FILES_NAMES = {
    "vocab_file": "vocab.json",
    "merges_file": "merges.txt",
    "tokenizer_file": "tokenizer.json",
}

PRETRAINED_VOCAB_FILES_MAP = {
    "vocab_file": {},
    "merges_file": {},
    "tokenizer_file": {},
}

PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES = {}


class ByteLevelBPETokenizerFast(RobertaTokenizerFast):
    vocab_files_names = VOCAB_FILES_NAMES
    pretrained_vocab_files_map = PRETRAINED_VOCAB_FILES_MAP
    max_model_input_sizes = PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES
    model_input_names = ["attention_mask"]

    def __init__(
        self,
        vocab_file: Text,
        merges_file: Text,
        tokenizer_file: Optional[Text] = None,
        errors: Text = "replace",
        unk_token: Token = "<unk>",
        bos_token: Token = "<s>",
        eos_token: Token = "</s>",
        pad_token: Token = "<pad>",
        sep_token: Token = "</s>",
        cls_token: Token = "<s>",
        mask_token: Token = "<mask>",
        add_prefix_space: bool = False,
        trim_offsets: bool = True,
        lowercase: bool = False,
        **kwargs: Any,
    ) -> None:
        # pylint: disable=too-many-arguments, too-many-locals
        super().__init__(
            vocab_file,
            merges_file,
            tokenizer_file=tokenizer_file,
            errors=errors,
            bos_token=bos_token,
            eos_token=eos_token,
            sep_token=sep_token,
            cls_token=cls_token,
            unk_token=unk_token,
            pad_token=pad_token,
            mask_token=mask_token,
            add_prefix_space=add_prefix_space,
            trim_offsets=trim_offsets,
            lowercase=lowercase,
            **kwargs,
        )

        # setup tokenizer normalization
        normalizer = Lowercase() if lowercase else Sequence([])
        self.backend_tokenizer.normalizer = normalizer
        self.lowercase = lowercase

        # setup tokenizer pre-tokenization
        pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=add_prefix_space)
        self.backend_tokenizer.pre_tokenizer = pre_tokenizer
        self.add_prefix_space = add_prefix_space

        # setup tokenizer post-processing
        post_processor = processors.ByteLevel(trim_offsets=trim_offsets)
        self.backend_tokenizer.post_processor = post_processor
        self.trim_offsets = trim_offsets
