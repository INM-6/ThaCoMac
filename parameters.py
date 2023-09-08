# search keywords lexicon
# search in all fields
# "" means exact match, otherwise the search engine will treat every word separately

# search_kws_lexicon = 
# (macaque OR macaca OR "rhesus monkey") AND 
# (thalamus OR thalamic OR thalamocortical OR "thalamo-cortical" OR corticothalamic OR "cortico-thalamic")

websites_gs = {
    'neurology.org', 'bmj.com', 'wiley.com', 'oup.com', 'springer.com', 'mdpi.com', 
    'biomedcentral.com', 'sagepub.com', 'cambridge.org', 'wfu.edu', 'cell.com', 'europepmc.org', 
    'aspetjournals.org', 'psych.ac.cn', 'biorxiv.org', 'ieee.org', 'jstor.org', 'royalsocietypublishing.org', 
    'bu.edu', 'lww.com', 'eneuro.org', 'jst.go.jp', 'plos.org', 'ncbi.nlm.nih.gov', 'liebertpub.com', 
    'psychiatryonline.org', 'sciencedirect.com', 'psycnet.apa.org', 'degruyter.com', 'nature.com', 'jamanetwork.com', 
    'karger.com', 'tandfonline.com', 'physiology.org', 'pnas.org', 'jneurosci.org', 'thejns.org', 
    'agro.icm.edu.pl', 'elifesciences.org', 'frontiersin.org', 'science.org'}


# websites
websites = [
    'www.ncbi.nlm.nih.gov', 'linkinghub.elsevier.com', 'wiley.com', 'link.springer.com', 'journals.physiology.org', 
    'academic.oup.com', 'www.cambridge.org', 'karger.com', 'journals.lww.com', 'www.nature.com', 'www.science.org', 
    'www.tandfonline.com', 'journals.sagepub.com', 'jamanetwork.com', 'neurology.org', 'www.biorxiv.org', 
    'europepmc.org', 'iovs.arvojournals.org', 'royalsocietypublishing.org', 'psychiatryonline.org', 'direct.mit.edu', 
    'www.jstage.jst.go.jp', 'thejns.org', 'www.annualreviews.org', 'aspetjournals.org', 'jnm.snmjournals.org', 
    'www.ahajournals.org', 'pubs.acs.org', 'www.thieme-connect.de', 'pubs.asahq.org', 
    'www.ingentaconnect.com', 'ujms.net', 'journals.biologists.com', 'www.microbiologyresearch.org', 
    'journals.aps.org', 'www.imrpress.com', 'www.researchsquare.com', 'ieeexplore.ieee.org', 'papers.ssrn.com', 
    'www.jneurosci.org'
]


# on-topic keyword lexicon
on_topic_kws = [
    'thalamocortical', 'thalamo-cortical', 'corticothalamic', 'cortico-thalamic',
    'tracing', 'tracer', 'tract tracing', 'tract-tracing', 'axonal tracing', 'neural tracing', 'anatomical tracing', 'neuroanatomical tracing', 'anatomical neural tracing',
    "staining", "dye",
    'thalamus', 'cortex', 'thalamic', 'cortical',  
    'connection', 'projection', 'connectivity', 'connectome', "anterograde", "retrograde", "injection", "injected", "injecting", "inject"]
# pathway


on_topic_kws_weights = {
    'thalamocortical': 20, 'thalamo-cortical': 20, 'thalamic': 20, 'thalamus': 20,
    'tracing': 15, 'tracer': 15, 'tract tracing': 15, 'tract-tracing': 15, 'axonal tracing': 15, 'neural tracing': 15, 
    'anatomical tracing': 15, 'anatomical neural tracing': 15, 'neuroanatomical tracing': 15, "anterograde": 15, "retrograde": 15,
    "injection": 10, "injected": 10, "injecting": 10, "inject": 10, 
    'corticothalamic': 5, 'cortico-thalamic': 5, "staining": 5, "dye": 5,
    'connection': 5, 'projection': 5, 'connectivity': 5, 
    'thalamus': 2, 'cortex': 2, 'cortical': 2, 
    'connectome': 1}
# --------------------start of test code--------------------
# if len(on_topic_kws) != len(on_topic_kws_weights):
#     raise ValueError("Length of on_topic_kws and on_topic_kws_weights should be the same.")
# ---------------------end of test code---------------------


# ChatGPT, queries for relatedness of topic
ChatGPT_related_queries = ['Does the given text include information of thalamocotical connection?',
                           'Does this paper provide data of thalamocotical connection?',
                           'Does the given text include information of connection between thalamus and cortex?']


# meta categories, keywords, and correspond ChatGPT queries
meta_categ = ['DOI', 'Publication_link', 'pdf_link', 'Authors', 'Year', 'Country', 'Affiliation', 
              'Title', 'Abstract', 'Keywords', 
              'Thalamic_parcellation_scheme', 'Cortical_parcellation_scheme', 
              'Thalamic_area_focused', 'Cortical_area_focused',
              'Stereotaxic_space', 'Type_of_data']


meta_categ_kws = ['parcellation', 'cortical', 'thalamic', 'stereotaxic']


ChatGPT_meta_categ_quries = ['what is the parcellation scheme this paper used for cortex?', 
                             'what is the parcellation scheme this paper used for thalamus?',
                             'which areas of the thalamus does this study include?',
                             'which areas of the cortex does this study include?',
                             'Does this paper mention stereotaxic space the studies used?',
                             'Does this paper']