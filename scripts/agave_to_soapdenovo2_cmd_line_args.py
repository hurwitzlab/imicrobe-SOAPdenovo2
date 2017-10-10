"""
Usage:

  python agave_to_soapdenovo2_cmd_line-args.py \
      config_file_path \
      -o output-graph \
      -q1 /path/to/forward/reads \
      -q2 /path/to/reverse/reads \
      -some more -options

The config_file_path argument must specify an existing SOAPdenovo2 configuration file, which will be
extended (overwritten) with the file paths specified by -f1, -f2, -q1, -q2, et al., command line arguments.

Convert Agave app arguments such as

  -q1 file1 -q2 file2

to SOAPdenovo2 configuration file lines such as

  q1=file1
  q2=file2

The required -o argument specifies the output graph prefix.

Since this script may also be invoked in contexts other than an Agave job it should
leave normal SOAPdenovo2 command line args alone.

"""
import argparse
import io
import os
import sys


def get_args(argv):
    """
    The first positional argument is the configuration file. Remaining command line arguments
    either need conversion from Agave repeated-option format or can be passed directly to
    SOAPdenovo2.

    :return: (1-ple of config file, tuple of everything else)
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config-fp', required=True, help='Path to configuration file.')
    arg_parser.add_argument('--output-dir', required=True, help='Path to output directory')
    arg_parser.add_argument('--output-graph-prefix', required=True, help='Prefix for output graph files.')
    # parse_known_args does not ignore the first element of argv so remove it first
    # otherwise the config_fp parameter is set to this script
    return arg_parser.parse_known_args(args=argv[1:])


def extend_config_file_content(config_file_content, agave_cmd_line_args):
    # the options in this table need conversion from Agave to soapdenovo2
    input_option_table = {
        '-b': list(),
        '-f': list(),
        '-p': list(),
        '-q': list(),
        '-f1': list(),
        '-f2': list(),
        '-q1': list(),
        '-q2': list()
    }

    additional_args_list = []

    # segregate args from unknown_arg_list into the
    # input_option_table or the additional_args_list
    unknown_arg_list = list(agave_cmd_line_args)
    while len(unknown_arg_list) > 0:
        next_arg = unknown_arg_list.pop(0)
        if next_arg in input_option_table.keys():
            input_option_table[next_arg].append(unknown_arg_list.pop(0))
        else:
            additional_args_list.append(next_arg)

    input_option_table['f12'] = list(zip(input_option_table['-f1'], input_option_table['-f2']))
    input_option_table['q12'] = list(zip(input_option_table['-q1'], input_option_table['-q2']))

    # combine FASTA and FASTQ paired-end lists
    extended_config_file_buffer = io.StringIO()
    # remove empty lines because this may cause trouble with SOAPdenovo2 (fact check?)
    for line in config_file_content.splitlines():
      stripped_line = line.strip()
      if len(stripped_line) == 0:
          pass
      else:
        extended_config_file_buffer.write(stripped_line)
        extended_config_file_buffer.write('\n')

    for (dash, opt), arg_list in [(opt_, input_option_table[opt_]) for opt_ in ('-f', '-q', '-b', '-p')]:
        while len(arg_list) > 0:
            fp = arg_list.pop(0)
            extended_config_file_buffer.write('{}={}\n'.format(opt, fp))

    for (opt, *_), arg_list in [(opt_, input_option_table[opt_]) for opt_ in ('f12', 'q12')]:
        while len(arg_list) > 0:
            fp1, fp2 = arg_list.pop(0)
            extended_config_file_buffer.write('{}1={}\n'.format(opt, fp1))
            extended_config_file_buffer.write('{}2={}\n'.format(opt, fp2))

    return extended_config_file_buffer.getvalue()


def get_soapdenovo2_cmd_line(script_args):
    return 'all -s {} -o {}'.format(
        script_args.config_fp,
        os.path.join(
            script_args.output_dir,
            script_args.output_graph_prefix
        )
    )


if __name__ == '__main__':
    # parse arguments - get the config file path and everything else
    script_args, all_other_args = get_args(sys.argv)
    # read the config file
    config_file_content = io.StringIO()
    with open(script_args.config_fp, 'rt') as config_file:
        config_file_content.write(config_file.read())
    extended_config_file_content = extend_config_file_content(config_file_content.getvalue(), all_other_args)
    # overwrite config_fp with the extended config file
    with open(script_args.config_fp, 'wt') as config_file:
        config_file.write(extended_config_file_content)

    soapdenovo2_cmd_line = get_soapdenovo2_cmd_line(script_args)
    print(soapdenovo2_cmd_line)


def test_agave_to_soapdenovo2_cmd_line_args():
    script_args, cmd_line_args = get_args(
        [
            'this_script.py',
            '--config-fp', 'configfile',
            '--output-dir', '/output/dir',
            '--output-graph-prefix', 'output.graph.prefix',
            '-f1', 'file1.fa',
            '-f2', 'file2.fa'
        ]
    )
    assert script_args.config_fp == 'configfile'
    assert script_args.output_dir == '/output/dir'
    assert script_args.output_graph_prefix == 'output.graph.prefix'

    assert get_soapdenovo2_cmd_line(script_args) == 'all -s configfile -o /output/dir/output.graph.prefix'

    assert cmd_line_args == ['-f1', 'file1.fa', '-f2', 'file2.fa']


def test_single_end_fasta_conversions():
    # throw in some extra newlines to see that they are removed
    extended_config_file_content = extend_config_file_content(
        '[LIB]\n\n',
        ['-f', 'file1.fa']
    )

    assert extended_config_file_content == """\
[LIB]
f=file1.fa
"""

    extended_config_file_content = extend_config_file_content(
            '[LIB]\n\n',
            ['-f', 'file1.fa', '-f', 'file2.fa']
        )

    assert extended_config_file_content == """\
[LIB]
f=file1.fa
f=file2.fa
"""


def test_single_end_fastq_conversions():
    # throw in some extra newlines to see that they are removed
    extended_config_file_content = extend_config_file_content(
        '[LIB]\n\n',
        ['-q', 'file1.fq', '-q', 'file2.fq', '-q', 'file3.fq']
    )

    assert extended_config_file_content == """\
[LIB]
q=file1.fq
q=file2.fq
q=file3.fq
"""


def test_single_file_paired_end_fasta_conversions():
    # throw in some extra newlines to see that they are removed
    extended_config_file_content = extend_config_file_content(
        '[LIB]\n\n',
        ['-p', 'file1.fa', '-p', 'file2.fa']
    )

    assert extended_config_file_content == """\
[LIB]
p=file1.fa
p=file2.fa
"""


def test_single_file_paired_end_bam_conversions():
    # throw in some extra newlines to see that they are removed
    extended_config_file_content = extend_config_file_content(
        '[LIB]\n\n',
        ['-b', 'file1.bam', '-b', 'file2.bam']
    )

    assert extended_config_file_content == """\
[LIB]
b=file1.bam
b=file2.bam
"""


def test_paired_end_fasta_conversions():
    # throw in some extra newlines to see that they are removed
    extended_config_file_content = extend_config_file_content(
        '[LIB]\n\n',
        ['-f1', 'file1.fa', '-f2', 'file2.fa']
    )

    assert extended_config_file_content == """\
[LIB]
f1=file1.fa
f2=file2.fa
"""


def test_paired_end_fastq_conversions():
    extended_config_file_content = extend_config_file_content(
        '[LIB]',
        ['-q1', 'file1.fq', '-q2', 'file2.fq', '-q1', 'file3.fq', '-q2', 'file4.fq']
    )

    assert extended_config_file_content == """\
[LIB]
q1=file1.fq
q2=file2.fq
q1=file3.fq
q2=file4.fq
"""
