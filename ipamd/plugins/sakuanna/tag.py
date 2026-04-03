from ipamd.public.models.data import Vector


def func(protein, tags):
    tag_data = []
    default_tag = 'normal'
    for tag in tags:
        if tags[tag] == 'rest':
            default_tag = tag
            tags.pop(tag)
            break
    for _ in protein:
        tag_data.append(default_tag)
    seq = protein.sequence
    for tag in tags:
        for sub_seq in tags[tag]:
            start = -1
            while True:
                start += 1
                start = seq.find(sub_seq, start)
                if start == -1:
                    break
                for i in range(len(sub_seq)):
                        tag_data[start + i] = tag
    res = Vector(
        title=f'Protein Component Tags of {protein.name}',
        data=tag_data,
        x_label=f'Amino Acid Index of {protein.name}',
        y_label='Tag'
    )
    return res