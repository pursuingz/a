import re
import struct
import subprocess
import py7zr

# define the size of sub-segments
subseg_size = 4

def find_segments(sequence):
    """
    find all sub-segments of length subseg_size in sequence
    """
    segments = {}
    for i in range(len(sequence)-subseg_size+1):
        subseg = sequence[i:i+subseg_size]
        if subseg in segments:
            segments[subseg].append(i)
        else:
            segments[subseg] = [i]
    return segments

def compress(sequence):
    # set up variables to store compressed data and metadata
    compressed_seq = ''
    Substring_info = ''
    lower_case_pos = []
    lower_case_info = ''
    non_ACGT_pos = []
    non_ACGT_info = ''
    non_ACGT_line = ''
    header_info = ''
    header_pos = []

    # separate header from sequence
    header = ''
    for i in range(len(sequence)):
        if sequence[i] == '>':
            start = i
            end = sequence.find('\n', start)
            header += sequence[start:end]
            header_info += f'{len(header)} {header}\n'
            header = ''

    # remove header from sequence
    sequence = re.sub(r'>.+?\n', '', sequence)
    header_pos.append(0)
    i=0
    while(i<len(sequence)):
        if sequence[i] == '\n':
            sequence = sequence[:i] + sequence[i+1:]
            header_pos.append(i)
            header_info += f'{i}\n'
        i+=1
    
    # process lower case characters
    matches = re.finditer(r'[a-z]+', sequence)
    for match in matches:
        lower_case_pos.append((match.start(), match.end()-1))
        lower_case_info += f'{match.start()} {match.end()-1}\n'
        sequence = sequence[:match.start()] + match.group().upper() + sequence[match.end():]
    # process non-ACGT characters
    
    i = 0
    while(i<len(sequence)-1):
        if sequence[i] != 'A' and sequence[i]!= 'C' and sequence[i]!= 'G' and sequence[i]!= 'T': 	
            start=i
            end = i+1
            print(end)
            while sequence[end] != 'A' and sequence[end] != 'C' and sequence[end] != 'G' and sequence[end] != 'T':
                
                end+=1
            non_ACGT_pos.append((start))
            non_ACGT_line = sequence[start:end]
            non_ACGT_info += f'{start} {non_ACGT_line}\n'
            sequence = sequence[:start] + sequence[end:]
        i += 1

    # compress sequence using statistical model and arithmetic coding
    m=6
    while m > 0:
        # find all subsegments in the remaining sequence
        m -= 1
        segments = find_segments(sequence)
        # loop through all subsegments to find the most frequent segment
        max_freq = 0
        max_seg = ''
        for seg, pos in segments.items():
            freq = len(pos)
            if freq > max_freq:
                max_freq = freq
                max_seg = seg

        Substring_info += f'{max_seg}'
        for pos in segments[max_seg]:
            Substring_info += f' {pos}'
        Substring_info += f'\n'
        sequence = sequence.replace(max_seg, '')

    # compresse in binary
    binary_dict = {'A': '00', 'T': '01', 'C': '10', 'G': '11', '\n': ''}
    for base in sequence:
        compressed_seq += binary_dict[base]
    # concatenate all compressed bytes and return+ compressed_lower_case + compressed_non_ACGT
    return header_info , lower_case_info , non_ACGT_info , Substring_info , compressed_seq 
