
with open('test.txt', 'r') as f:
    content = f.readlines()
    out_content = ""
    out_content2 = ""
    for i in range(len(content)):
        time = content[i].split('-')
        start_time = time[0].split(':')
        start_hour = start_time[0]
        start_min = start_time[1]

        end_time = time[1].split(':')
        end_hour = end_time[0]
        end_min = end_time[1].strip()
        out_content += str(i)+': '+'(%s, %s),\n' % (start_hour, start_min)
        out_content2 += str(i)+': '+'(%s, %s),\n' % (end_hour, end_min)
    # print(out_content)
    print(out_content2)
    outfile = open('test1.txt', 'w')
    outfile.write((out_content+out_content2))
