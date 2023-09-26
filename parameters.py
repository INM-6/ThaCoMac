# literature ranking
# ===================================================================================================================================
# # on-topic keyword lexicon
# on_topic_kws_weights = {
#     "macaque": 30,
#     'thalamocortical': 20, 'thalamo-cortical': 20, 'thalamic': 20, 'thalamus': 20, 'corticothalamic': 5, 'cortico-thalamic': 5, 
#     'tracing': 15, 'tracer': 15, 'tract tracing': 15, 'tract-tracing': 15, 'axonal tracing': 15, 'neural tracing': 15, 
#     'anatomical tracing': 15, 'anatomical neural tracing': 15, 'neuroanatomical tracing': 15, "anterograde": 15, "retrograde": 15,
#     "injection": 10, "injected": 10, "injecting": 10, "inject": 10, 
#     "staining": 5, "dye": 5, 'connection': 5, 'projection': 5, 'connectivity': 5, 
#     'thalamus': 2, 'cortex': 2, 'cortical': 2, 
#     'connectome': 1}

text_length_to_extract = 1000

species = 3
tc_ct = 6
thalam = 6
cortex = 0.001
method = 6
connectivity = 5

# 6 groups of keywords and their weights
ranking_params_weights = {
   'species': species, "tc_ct": tc_ct, "thalam": thalam, "cortex": cortex, "method": method, "connectivity": connectivity
   }

ranking_params = ["species", "tc_ct", "thalam", "cortex", "method", "connectivity"]

species_related = [
   'rhesus', 'macaque', 'macaca'
   ]
tc_ct_related = [
      'thalamocortical', 'thalamo-cortical', 'corticothalamic', 'cortico-thalamic'
   ]
thalam_related = [
      'thalam', 'mediodorsal', 'MD', 'pulvinar', 'posteroventral', 'ventral lateral', 'ventral-lateral', 'ventrolateral', 'VLpv', 'anterior thalamic nuclei', 'laterodorsal', 'anteroventral', 'anteromedial', 'suprageniculate', 'SGN', 'medial geniculate', 'MG', 'MGv', 'MGd', 'MGm', 'ventroposterolateral', 'ventro-posterior lateral', 'VPL', 'subcortical', 'lateral geniculate nucleus', 'LGN'
   ]
cortex_related = [
      'cortex', 'cortical', 'cortices', 'V1', 
   ]
method_related = [
   'tract', 'tracing', 'traced', 'tracer', "anterograde", "retrograde", 'inject', 'horseradish peroxidase', 'fluorescent', 'cholera toxin', 'PHA-L', 'WGA-HRP', 'BDA', 'amino acids', 'PHA-L', 'leucine', 'proline', 'lesion', 'autoradiographic', 'diﬀusion MRI', 'fMRI', 'staining', 'dye'
   ]
connectivity_related = [
      'connect', 'projection', 'projecting', 'projected', 'afferent', 'efferent', 'fibers', 'input', 'pathway', 
   ]
# ===================================================================================================================================




# search keywords lexicon
# ===================================================================================================================================
# search_kws_lexicon = (macaque OR macaca OR "rhesus monkey") AND (thalamus OR thalamic OR thalamocortical OR "thalamo-cortical" OR corticothalamic OR "cortico-thalamic")

# search in all fields
# "" means exact match, otherwise the search engine will treat every word separately
# ===================================================================================================================================




# extract info websites
# ===================================================================================================================================
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
    # newlly added
    'www.jneurosci.org', 'biomedcentral.com'
]
# ===================================================================================================================================




# download websites
# ===================================================================================================================================
download_by_request = [
    'aspetjournals.org', 'citeseerx.ist.psu.edu', 'www.nature.com', 'karger.com', 'ahuman.org', 'www.researchsquare.com',
    'link.springer.com', 'www.ijpp.com', 'www.bu.edu', 'www.ncbi.nlm.nih.gov', 'www.thieme-connect.de', 'deepblue.lib.umich.edu', 
    'bpb-us-e1.wpmucdn.com', 'zsp.com.pk', 'journals.biologists.com', 'journals.aps.org', 'academic.oup.com', 'www.biorxiv.org', 
    'enpubs.faculty.ucdavis.edu', 'n.neurology.org', 'ruor.uottawa.ca', 'www.jstage.jst.go.jp', 'synapse.koreamed.org', 'www.jneurosci.org', 
    'pubs.asahq.org', 'biomedcentral.com', 'direct.mit.edu', 'jnm.snmjournals.org'
 ]

download_pdf_by_button = ['www.ahajournals.org', 'psychiatryonline.org']


download_from = [
    'www.microbiologyresearch.org', 'europepmc.org', 'papers.ssrn.com', 'www.ingentaconnect.com', 'journals.lww.com']

# 'linkinghub.elsevier.com'

# 'physiology.org'

# 'journals.sagepub.com'

download_not_possible = ['royalsocietypublishing.org', 'jamanetwork.com', 'www.cell.com', 'ieeexplore.ieee.org', 'www.researchgate.net']

download_pdf_by_a = ['wiley.com', 'www.science.org', 'tandfonline.com', 'acs.org']

download_pdf_by_driver = ['iovs.arvojournals.org', 'www.imrpress.com', 'www.hifo.uzh.ch', 'ujms.net', 'www.annualreviews.org', 'thejns.org']
# ===================================================================================================================================




# extract metadata categories
# ===================================================================================================================================
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
# ===================================================================================================================================