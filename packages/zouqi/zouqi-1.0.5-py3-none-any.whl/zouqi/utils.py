def message_box(title, sections, aligner="<"):
    lines = [title] + [s for section in sections for s in section.splitlines()]
    widest = max(map(len, lines))
    width = widest + 4

    nb = width - 2  # number of blanks
    border = f"│{{: ^{nb}}}│"

    out = []
    out.append("┌" + "─" * nb + "┐")
    out.append(border.format(title.capitalize()))
    out.append("├" + "─" * nb + "┤")

    for i, section in enumerate(sections):
        for line in section.splitlines():
            out.append(border.replace("^", aligner).format(line.strip()))

        if i < len(sections) - 1:
            out.append("├" + "─" * nb + "┤")
        else:
            out.append("└" + "─" * nb + "┘")

    return "\n".join(out)


def print_args(args, command_args):
    args, command_args = map(vars, [args, command_args])
    args = [f"{k}: {v}" for k, v in sorted(args.items())]
    command_args = [f"{k}: {v}" for k, v in sorted(command_args.items())]
    sections = []
    if len(args):
        sections.append("\n".join(args))
    if len(command_args):
        sections.append("\n".join(command_args))
    print(message_box("Arguments", sections))
