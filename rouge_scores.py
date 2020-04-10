from rouge import Rouge
from rouge_score import rouge_scorer
import matplotlib.pyplot as plt


def rouge_score_us299_vs_us253():
    reference_us299 = 'The present disclosure relates to a fabricating method of light guiding plate, and a backlight ' \
                      'module and a display device. The embodiment of the present disclosure provides a fabricating ' \
                      'method of grid points on a light guiding plate. The method includes following steps a layer of ' \
                      'photosensitive resin is formed on a mold for the light guiding plate. The layer of photosensitive ' \
                      'resin is subjected to a photolithography process to form grid points on the light guiding ' \
                      'plate.Steps are forming a layer of photosensitive material on a mold for the light guiding plate; ' \
                      'and performing photolithography on the photosensitive material in order to form grid points on ' \
                      'the light guiding plate. The method according to claim wherein the step of S further comprises following steps of S ' \
                      'performing a refaction on the mold for the light guid ing plate S applying the photosensitive '
    reference_us253 = 'This invention relates to a molded optical panel for use in, Such as, for example, a back light ' \
                      'or front light panel of liquid crystal display.The optical pattern is directly formed by making ' \
                      'use of a mold and a molded pattern of a photoSensitive heat-resistant resin formed by the use of ' \
                      'a photoresist method via a pattern film. The photo resistant resin is a positive type and the ' \
                      'pattern film is an optical pattern element.The optical pattern is formed as a projected pattern ' \
                      'having projected optical pattern elements. The photosensitive heat-resistant resin may be ' \
                      'negative type and the pattern film may be a positive film, thereby the optical pattern is formed ' \
                      'as a projected pattern having projected optical pattern elements. The formation of the molded ' \
                      'pattern on the mold base by the use of the positive-type ' \
                      'photosensitive heat-resistant resin comprises the steps of coating the mold base with the ' \
                      'positivetype photosensitive heat-resistant resin to form the photoresist ﬁlm on its surface '

    hypothesis_patcom_us299 = 'Claim 1. A fabricating method of grid points on a light guiding plate, comprising following steps ' \
                              'of: S1, forming a layer of photosensitive ma-terial on a mold for the light guiding plate; and S2, ' \
                              'performing photolithography on the photosensitive material in order to form grid points on the ' \
                              'light guiding plate. Claim 2. The method according to claim 1, wherein the photosensitive material ' \
                              'is a photosensitive resist. '
    hypothesis_patcom_us253 = 'The formation of the molded pattern on the mold base by the use of the positive-type ' \
                              'photosensitive heat-resistant resin comprises the steps of coating the mold base with the ' \
                              'positivetype photosensitive heat-resistant resin to form the photoresist ﬁlm on its surface, ' \
                              'pre-heating the photoresist ﬁlm so as to harden slightly, exposing the applied photoresist ﬁlm to ' \
                              'light via the positive-type pattern ﬁlm for forming the optical pattern. '

    hypothesis_us299 = 'The method according to claim wherein the step of S further comprises following steps of S ' \
                       'performing a refaction on the mold for the light guid ing plate S applying the photosensitive ' \
                       'resist on the surface of the mold for the light guiding plate and S removing a solvent in the ' \
                       'photosensitive resist The method according to claim wherein in step S the photosensitive resist ' \
                       'is exposed with UV radiation and each grid point on the light guiding plate is a dome like recess ' \
                       'with a diameter D Al Designing grid points arrangement pattern of light guiding plate L ima oria ' \
                       'A Preparing the film with the designed grid points arrangement pattern Fabricating grid points on ' \
                       'mold for light guiding plate Loading the mold for the light guiding plate A formed with grid ' \
                       'points into a mold case for the light guiding plate and obtaining the light guiding plate by an ' \
                       'injection molding process with the mold Fig.'

    hypothesis_us253 = 'A molded optical panel as defined in claim wherein Said photoSensitive heatresistant resin is ' \
                       'a positive type and Said pattern film is a positive film Such that Said optical pattern is ' \
                       'formed as a concave pattern having concave optical pattern elements In addition the molded ' \
                       'optical panel of the present inventions can provide the preferable shape of the optical ' \
                       'pattern and makes the light guiding of for example an edge light panel high luminance and ' \
                       'high uniformity either by forming the optical pattern high density or by controlling the ' \
                       'light guiding of incident light in the direction distant from the light Source The present ' \
                       'inventor has been developed to address the first and Second problems as described above ' \
                       'wherein the following facts were determined Since the molded pattern can be formed directly ' \
                       'on the mold base by a photosensitive heatresistant resin wherein the molded pattern is formed ' \
                       'on the mold base using a photoresist method via the pattern film by making use of the ' \
                       'photoSensitive heatresistant resin the problems resulting from charging of the heat resistant ' \
                       'resin when the molded pattern is formed indirectly can be solved A method as defined in claim ' \
                       'wherein said optical pattern is a light guiding pattern Such that Said light guiding pattern ' \
                       'is formed by varying nonStepwise a diameter Side length density of the light guiding elements ' \
                       'So as to perform light guiding inversely proportional to an amount of incident light from a ' \
                       'light incident edge face toward a position distant from Said light incident edge face and ' \
                       'control light The optical pattern acts as a light guiding pattern and is formed by changing ' \
                       'non Stepwise diameter density of the optical pattern element comprising dots or lines So as ' \
                       'to perform light guiding inversely proportional to an amount of incident light from a light ' \
                       'incident edge face of the optical panel toward a position distant from the light incident ' \
                       'edge face to perform light guiding control The face illuminator comprises a molded edge light ' \
                       'panel having one Surface that is formed integrally with an optical pattern a reflector placed ' \
                       'on a back Surface of molded edge light panel and a light diffusing element placed on the ' \
                       'light the alight Source of a linear light Source Such as for example a cold cathode emitting ' \
                       'Surface of the molded edge light panel The face illuminator is provided fluorescent tube ' \
                       'located adjacently to a light incident edge face of the mold edge light panel The face ' \
                       'illuminator guides incident light Supplied from the light Source to the light incident edge ' \
                       'face So as to illuminate Secondarily the whole Surface area of the edge light panel by means ' \
                       'of the light guiding pattern'

    dic = {}
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_us299, hypothesis_us299)
    dic['Patent Comparision'] = scores['rouge1'].fmeasure
    scores = scorer.score(reference_us253, hypothesis_us253)
    dic['Patent Comparision'] = (dic['Patent Comparision'] + scores['rouge1'].fmeasure) / 2

    scores = scorer.score(reference_us253, hypothesis_patcom_us253)
    dic['Patcom'] = scores['rouge1'].fmeasure
    scores = scorer.score(reference_us299, hypothesis_patcom_us299)
    dic['Patent Comparision'] = (dic['Patent Comparision'] + scores['rouge1'].fmeasure) / 2
    print(dic)
    return dic


def rouge_score_us299_vs_us520():
    reference_us299 = 'The present disclosure relates to a fabricating method of light guiding plate, and a backlight ' \
                      'module and a display device. The embodiment of the present disclosure provides a fabricating ' \
                      'method of grid points on a light guiding plate. The method includes following steps: a layer ' \
                      'of photosensitive resin is formed on a mold for the light guiding plate. The layer of ' \
                      'photosensitive resin is subjected to a photolithography process to form grid points on the ' \
                      'light guiding plate.Steps are forming a layer of photosensitive material on a mold for the ' \
                      'light guiding plate; and performing photolithography on the photosensitive material in order ' \
                      'to form grid points on the light guiding plate. '

    reference_us520 = 'An object of the present invention is to provide a die suitable for producing an optical panel ' \
                      'having an optical pattern (e.g. dots or lines) integrally formed on at least one side of the ' \
                      'optical panel, which is used in a backlight or front light for a liquid crystal display. the ' \
                      'die comprising a metal Substrate and a molding pattern corresponding to said optical pattern ' \
                      'and formed of a photosensitive heat-resistant resin on one side of Surfaces of the metal ' \
                      'substrate, wherein the whole of the surface having the molding pattern of the metal substrate ' \
                      'is covered with a layer of said heat-resistant resin. the process comprising the steps of ' \
                      'setting, on at least one of the two surfaces of a mold, a molding die comprising a metal ' \
                      'Substrate and a molding pattern corresponding to the optical pattern of the optical panel and ' \
                      'formed of a photosensitive heat-resistant resin on one side of surfaces of the metal ' \
                      'substrate. An object of the present invention is to provide a die suitable ' \
                      'for producing an optical panel having an optical pattern integrally formed on at least one ' \
                      'side of the optical panel which is for example an edge light panel or a light diffusion panel ' \
                      'which is used in a backlight or front light for a liquid crystal display and various ' \
                      'illuminators'

    hypothesis_patcom_us299 = 'Claim 5. The method according to claim 2, wherein the step of S2 further comprises ' \
                              'following steps of: S21 using a ﬁlm formed with grid points arrangement pattern as a ' \
                              'mask, S22 sequentially performing exposing and developing process on the ' \
                              'photosensitive resist in order to form a grid points pattern on the photosensitive ' \
                              'resin, and S23 curing the photosensitive resist and removing residual solvent and ' \
                              'moisture. '
    hypothesis_patcom_us520 = 'a development step in which the photosensitive heat-resistant resin layer 12 exposed ' \
                              'is developed; a rinsing step in which the portions removed by the development are ' \
                              'rinsed away; and a baking step in which the pattern formed by the development is baked ' \
                              'at a high temperature to cure the photosensitive heat-resistant resin and form a ' \
                              'raised or depressed pattern... '

    hypothesis_us299 = 'In one example the step of S further includes fol lowing steps S the photosensitive resin is ' \
                       'Subjected to a sequential exposing process by irradiating UV lights and a developing process ' \
                       'using a film formed with grid points arrangement pattern as a mask in order to form grid ' \
                       'points pattern on the photosensitive resinUS A BACKLIGHT MODULE DISPLAY DEVICE AND ' \
                       'FABRICATING METHOD OF GRID POINTS ON LIGHT GUIDING PLATE AND LIGHT GUIDING PLATE FIELD The ' \
                       'present disclosure relates to a field of display technology in particular to a fabricating ' \
                       'method of grid points on light guiding plate a fabricating method of light guiding plate and ' \
                       'a backlight module and a display device. '

    hypothesis_us520 = 'The molding die can be set on the mold Surface for example by fixation by means of bolts ' \
                       'adhesion or Suction from the mold Surface side The light exposure step can be carried out for ' \
                       'example by a method in which the abovementioned photosensitive heatresistant resin layer or ' \
                       'is irradiated with gline light iline light or continuouswavelength light comprising them by ' \
                       'means of a stepper through the mask having a pattern corresponding to the optical pattern The ' \
                       'thus obtained molding die with the pattern was attached to one surface of an injection mold ' \
                       'and a methacrylate resin was injectionmolded by the use of the injection mold to produce a ' \
                       'lightguiding plate having a depressed pattern integrally formed on one side of surfaces of ' \
                       'the plate In this case the optical pattern is formed by forming pattern elements as ' \
                       'concavities on one side of Surfaces of the optical panel For molding an optical panel having ' \
                       'the pattern shown in and integrally formed thereon a die having a molding pattern formed as a ' \
                       'raised pattern on the Surface of the die is used which is shown in as a schematic vertical ' \
                       'crosssectional viewABSTRACT An object of the present invention is to provide a die suitable ' \
                       'for producing an optical panel having an optical pattern integrally formed on at least one ' \
                       'side of the optical panel which is for example an edge light panel or a light diffusion panel ' \
                       'which is used in a backlight or front light for a liquid crystal display and various ' \
                       'illuminators '

    dic = {}
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_us299, hypothesis_us299)
    dic['Patent Comparision'] = scores['rouge1'].fmeasure
    scores = scorer.score(reference_us520, hypothesis_us520)
    dic['Patent Comparision'] = (dic['Patent Comparision'] + scores['rouge1'].fmeasure) / 2

    scores = scorer.score(reference_us299, hypothesis_patcom_us299)
    dic['Patcom'] = scores['rouge1'].fmeasure
    scores = scorer.score(reference_us520, hypothesis_patcom_us520)
    dic['Patent Comparision'] = (dic['Patent Comparision'] + scores['rouge1'].fmeasure) / 2
    print(dic)
    return dic


def rouge_score_us689_vs_us775():
    reference_us689 = 'The invention relates to a jet regulator (1), comprising a jet regulator housing (2), ' \
                      'within the interior of which a jet regulation device (4) is provided.  In this case, ' \
                      'the shell-like jet regulator housing of the prior art jet regulator is made up of at least two ' \
                      'shell Sections designed as peripheral Segments. Pinsections are provided in each of these ' \
                      'shell parts that form pairs of impingers that are aligned with one another when the shell ' \
                      'parts are assembled.  The design of the prior art insertable component accord ing to DE-U297 ' \
                      '18 728, which contains shell parts and forms cylinder Sectors, also limits the design ' \
                      'possibilities, and thus also the areas of application of the prior art jet regulator, ' \
                      'as well as requiring expensive injection-molding tools. Thereby, the jet regulation device of ' \
                      'the prior art jet regu lator has an insertable component that contains the passage openings, ' \
                      'Said component consisting of at least two shell parts forming cylinder Sectors. '

    reference_us775 = 'A jet regulator comprising a jet fractionating device for dispersing an incoming water flow ' \
                      'into a multitude of individual jets of which at least one of the individual jets impinges at ' \
                      'least one nodal point of crisscrossing grid bars having downstream The jet regulator (1) ' \
                      'provides an improved fractionating of the incoming individual jets. This ' \
                      'jet fractionating device of the previ ously known jet regulator distributes the incoming ' \
                      'waterflow into a plurality of individual jets. The individual jets formed in the jet ' \
                      'fractionating device impinge several Subsequent metal sieves of a flow rectifier downstream, ' \
                      'which return the individual jets back into one uniform, bubbling combinedjet. In order to ' \
                      'aerate the individual jets several aeration openings are pro vided at the housing perimeter of ' \
                      'the jet regulator housing. Here, the jet fractionating device is aligned Such that the ' \
                      'individual jets each impinge a nodal point of criss-cross grid bars of a grid network arranged ' \
                      'downstream. The air necessary to aerate the water jet can be suctioned in through the aeration ' \
                      'openings. '

    hypothesis_patcom_us689 = 'A jet regulator comprising a jet fractionating device for dispersing an ' \
                              'incoming water flow into a multitude of individual jets, of which at least one of the ' \
                              'individual jets impinges at least one nodal point of criss-crossing grid bars (4, ' \
                              '5), having a downstream Surface located in and defining a single plane, ' \
                              'of a grid network arranged downstream from the jet fractionating device that is ' \
                              'provided as a separate construction partinajet regulator housing of the jet regulator A ventilated ' \
                              'jet regulator has ventilation openings at the peripheral cover of its jet regulator ' \
                              'housing. In order to keep dirt particles out of the interior of the housing  of the ' \
                              'jet regulator away from the aeration openings. an intake ﬁlter is placed. '

    hypothesis_patcom_us775 = 'A jet regulator comprising a jet fractionating device for dispersing an incoming water ' \
                              'ﬂow be arranged in reference to each other in approximately parallel cross-sectional ' \
                              'levels. However it is particularly advantageous when the deflect ing projection on the ' \
                              'side facing away from the aeration opening in the ﬂow direction downstream in ' \
                              'reference to the aeration openings,' \
                              'adeﬂecting with an extended angled deflection surface (10) at a side thereof in a flow ' \
                              'direction facing away from the aeration openings at the incoming side, are essentially ' \
                              'provided upstream with a cone-shape presieve, which separates the dirt particles entrained. '

    hypothesis_us689 = 'through show the jet regulator shown here can also be manufactured with little effort using ' \
                       'simple conventional manufacturing techniques wherein its jet regulation device and its flow ' \
                       'rectifier do not tend to Scale upUS B JET REGULATOR BACKGROUND This invention pertains to a ' \
                       'jet regulator with a jet regulator housing in whose interior a jet regulation device is ' \
                       'provided that has passage openings running approximately acroSS the passageway croSS Section ' \
                       'the openings being offset with respect to one another in the circumferential direction about ' \
                       'the jet regulator housing or in the direction of flow of the jet regulator wherein the jet ' \
                       'regulation device has at least one insertable component containing the passage openings The ' \
                       'ribs of the adjacent insertable components can be held at a minimal distance from one another ' \
                       'as necessary without a problem if the height of the Support ring of the insertable component ' \
                       'oriented in the direction of flow is larger than the height of the ribs and of the Support ' \
                       'rib if present and if the ribs and the Support rib are located within the peripheral contour ' \
                       'of the Support ring. '

    hypothesis_us775 = 'A jet regulator comprising a jet fractionating device for dispersing an incoming water flow ' \
                       'into a multitude of individual jets of which at least one of the individual jets impinges at ' \
                       'least one nodal point of crisscrossing grid bars having downstream Surfaces located in and ' \
                       'defin ing a single plane of a grid network arranged downstream from the jet fractionating ' \
                       'device that is provided as a separate construction partinajet regulator housing of the jet ' \
                       'regulator wherein the jet regulator is an aeratedjet regulator with the jet regulator housing ' \
                       'being provided at a housing perimeter with a plurality of circumferentially separated aera ' \
                       'tion openings and at an interior housing circumference in a flow direction below the aeration ' \
                       'openings the grid network including a deflection projection located to keep the waterjets ' \
                       'away from the aeration openings the deflection projection extending inwardly encircling an ' \
                       'inner circumference of an outer wall of the separately constructed grid network. '

    dic = {}
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_us689, hypothesis_us689)
    dic['Patent Comparision'] = scores['rouge1'].fmeasure
    scores = scorer.score(reference_us775, hypothesis_us775)
    dic['Patent Comparision'] = (dic['Patent Comparision'] + scores['rouge1'].fmeasure) / 2

    scores = scorer.score(reference_us689, hypothesis_patcom_us689)
    dic['Patcom'] = scores['rouge1'].fmeasure
    scores = scorer.score(reference_us775, hypothesis_patcom_us775)
    dic['Patent Comparision'] = (dic['Patent Comparision'] + scores['rouge1'].fmeasure) / 2
    print(dic)
    return dic


if __name__ == '__main__':
    score = {}
    score["Patent comparision"] = []
    score["Patcom"] = []
    score1=rouge_score_us299_vs_us253()
    score2=rouge_score_us299_vs_us520()
    score3=rouge_score_us689_vs_us775()

    score["Patent comparision"].append(score1["Patent Comparision"])
    score["Patcom"].append(score1["Patcom"])

    score["Patent comparision"].append(score2["Patent Comparision"])
    score["Patcom"].append(score2["Patcom"])

    score["Patent comparision"].append(score3["Patent Comparision"])
    score["Patcom"].append(score3["Patcom"])

    plt.plot(["us299_vs_us253","us299_vs_us520","us689_vs_us775"],score["Patent comparision"], label = "Patent comparision")
    plt.plot(["us299_vs_us253","us299_vs_us520","us689_vs_us775"],score["Patcom"], label = "Patcom")
    plt.legend()
    plt.show()
