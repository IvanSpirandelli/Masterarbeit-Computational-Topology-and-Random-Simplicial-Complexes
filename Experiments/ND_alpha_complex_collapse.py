import os
from datetime import datetime
from subprocess import Popen, PIPE

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper
from GudhiExtension.point_cloud_generator import point_cloud_generator

ch = point_cloud_generator()
outlines = []
now = datetime.now()
for i in range(5000):
    print("____"+str(i)+"____")
    ch.generate_n_points(1000,2)
    complex = alpha_complex_wrapper(ch.points)
    filtered_complex = complex.get_all_connected_filtration_steps()

    #TODO: This can probably be massively reduced, since we can't check intermediate steps? NO WE CAN. But randon_discrete_morse can't YET.
    with open('alpha_collapse.txt', 'w+') as script:
        script.truncate(0)
        script.write("use application 'topaz';\n")
        in_faces = ''
        for filter in filtered_complex:

            if(in_faces != ''):
                in_faces = in_faces[:-1] + ", " + str(filter)[1:]
            else:
                in_faces = str(filter)

            #script.write("print(random_discrete_morse(new SimplicialComplex(INPUT_FACES=>"+in_faces+"), save_collapsed=>'bla.xml'));\n")
        #If we do not indent it, we just get the final simplicial complex
        script.write("print(random_discrete_morse(new SimplicialComplex(INPUT_FACES=>"+in_faces+")));\n")

    polymake_process = Popen(['polymake', '--script', 'alpha_collapse.txt'], stdout=PIPE, stdin=PIPE)
    line, err = polymake_process.communicate()
    outlines.append(str(ch.points)+ '\n')
    outlines.append(str(line) + '\n')
    outlines.append('*********************************************\n')

with open(now.strftime("%j") + "_" + now.strftime("%H") +'_2D_alpha_complex_collaps_' + '.txt', 'w+') as f:
    for line in outlines:
        f.write(line)

    #f.write(str(ch.points)+ '\n')
    #polymake_process = Popen(['polymake', '--script', 'alpha_collapse.txt'], stdout = f, stdin =PIPE)
    #f.write("\n")


