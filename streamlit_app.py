import pandas as pd
import json
import plotly.express as px
import streamlit as st
from supabase import create_client, Client

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def read_data():
    response = supabase.table('elsevier_db').select("*").execute()
    df = pd.DataFrame(response.data)
    return df

df = read_data()

st.title("Accord Elsevier - données 01/01/24 - 14/10/26")

df_valide=df[(df['StatutEOAP'])=='Validé']
df_valide[['APCRemise']]=df_valide[['APCRemise']].fillna('')
df_valide_sans_frais=df_valide[(df_valide['APCRemise'])=='']
df_valide_remise=df_valide[(df_valide['APCRemise'])!='']

df_valide_sans_frais['DOI'].nunique()


st.header('Volume de publications par année et statut EOAP')
volume = pd.DataFrame(df[['Annee','StatutEOAP']].groupby('Annee').value_counts()).sort_values(by=['Annee','StatutEOAP'])

fig = px.bar(volume.reset_index(), x="Annee", y="count",
             color="StatutEOAP", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig)

st.header('Part de publications par année et statut EOAP')
volume_part=pd.DataFrame(df[['Annee','StatutEOAP']].groupby('Annee').value_counts(normalize=True).mul(100).round(2)).sort_values(by=['Annee','StatutEOAP'])
fig_part = px.bar(volume_part.reset_index(), x="Annee", y="proportion",
             color="StatutEOAP",
             barmode = 'stack')

st.plotly_chart(fig_part)

st.header('Part par domaine scientifique - validé : total')
domaines = pd.DataFrame(df_valide[['Annee','DomaineOpenAlex']])
domaines=domaines[(domaines['DomaineOpenAlex']!='False')]
domaines=domaines[(domaines['DomaineOpenAlex']!='Pas dans OpenAlex')]
domaines=(domaines.groupby('Annee').value_counts())

fig_domaines = px.bar(domaines.reset_index(), x="Annee", y="count",
             color="DomaineOpenAlex", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig_domaines)

st.header('Part par domaine scientifique - validé : inclus')
domaines_sans_frais = pd.DataFrame(df_valide_sans_frais[['Annee','DomaineOpenAlex']])
domaines_sans_frais=domaines_sans_frais[(domaines_sans_frais['DomaineOpenAlex']!='False')]
domaines_sans_frais=domaines_sans_frais[(domaines_sans_frais['DomaineOpenAlex']!='Pas dans OpenAlex')]
domaines_sans_frais=(domaines_sans_frais.groupby('Annee').value_counts())

fig_domaines_sans_frais = px.bar(domaines_sans_frais.reset_index(), x="Annee", y="count",
             color="DomaineOpenAlex", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig_domaines_sans_frais)

st.header('Part par domaine scientifique - validé : remisé')
domaines_remise = pd.DataFrame(df_valide_remise[['Annee','DomaineOpenAlex']])
domaines_remise=domaines_remise[(domaines_remise['DomaineOpenAlex']!='False')]
domaines_remise=domaines_remise[(domaines_remise['DomaineOpenAlex']!='Pas dans OpenAlex')]
domaines_remise=(domaines_remise.groupby('Annee').value_counts())

fig_domaines_remise = px.bar(domaines_remise.reset_index(), x="Annee", y="count",
             color="DomaineOpenAlex", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig_domaines_remise)

st.header('Répartition par modèle de publication - validé')
modeles = pd.DataFrame(df_valide[['Annee','ModeleRevue']])
modeles=(modeles.groupby('Annee').value_counts())

fig_modeles = px.bar(modeles.reset_index(), x="Annee", y="count",
             color="ModeleRevue", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig_modeles)

st.header('Répartition par licence')
licences = pd.DataFrame(df_valide[['Annee','Licence']])
licences=licences[(licences['Licence']!='not available at source')]
licences=(licences.groupby('Annee').value_counts())

fig_licences = px.bar(licences.reset_index(), x="Annee", y="count",
             color="Licence", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig_licences)

st.header('Répartition par bouquet')
bouquets = pd.DataFrame(df_valide[['Annee','Bouquet']])
bouquets=(bouquets.groupby('Annee').value_counts())

fig_bouquets = px.bar(bouquets.reset_index(), x="Annee", y="count",
             color="Bouquet", hover_data=['count'],
             barmode = 'group')
st.plotly_chart(fig_bouquets)

st.header('Evolution du prix catalogue moyen par modèle de revue et par an')
evolution_prix = pd.DataFrame(df_valide[['Annee','ModeleRevue','APCListPrice']])
evolution_prix=evolution_prix.groupby(['Annee','ModeleRevue']).mean(numeric_only=True)

fig_evol_prix = px.line(evolution_prix.reset_index(), x="Annee", y="APCListPrice",
             color="ModeleRevue", hover_data=['APCListPrice'])

fig_evol_prix.update_xaxes(range=['2024','2026'],dtick=1)
st.plotly_chart(fig_evol_prix)

st.header('Evolution des APC global payé remisé par an')
evolution_remise = pd.DataFrame(df_valide_remise[['Annee','APCRemise']])
evolution_remise=evolution_remise.groupby('Annee').sum()

fig_evol_remise = px.line(evolution_remise.reset_index(), x="Annee", y="APCRemise", hover_data=['APCRemise'])

fig_evol_remise.update_xaxes(range=['2024','2026'],dtick=1)
st.plotly_chart(fig_evol_remise)

st.header('Evolution du total de la dépense théorique par an')
evolution_sans_frais = pd.DataFrame(df_valide_sans_frais[['Annee','APCListPrice']])
evolution_sans_frais=evolution_sans_frais.groupby('Annee').sum()

fig_evol_theorique = px.line(evolution_sans_frais.reset_index(), x="Annee", y="APCListPrice", hover_data=['APCListPrice'])

fig_evol_theorique.update_xaxes(range=['2024','2026'],dtick=1)
st.plotly_chart(fig_evol_theorique)

st.header('Répartition des APC - prix catalogue')
boxplot_apc = px.box(df_valide['APCListPrice'], y="APCListPrice")
st.plotly_chart(boxplot_apc)

st.header('Classement des 20 premiers établissements par nombre de publication')
etab_total=pd.DataFrame(df_valide[['EtablissementValideur_FR']].groupby('EtablissementValideur_FR').value_counts())
etab_total['rank']=etab_total.rank(ascending=False,method='dense')
etab_total=etab_total.nsmallest(10,"rank").sort_values('count',ascending=True)

fig_etab_total = px.bar(etab_total.reset_index(), x="count", y="EtablissementValideur_FR", hover_data=['count'])
st.plotly_chart(fig_etab_total)

st.header('Classement des 20 premiers établissements par nombre de publication et par an')
etab_annee=pd.DataFrame(df_valide[['EtablissementValideur_FR']].groupby('EtablissementValideur_FR').value_counts())
etab_annee['rank']=etab_annee.rank(ascending=False,method='dense')
etab_annee=etab_annee.reset_index()
etab_annee=etab_annee.nsmallest(20,"rank").sort_values('count',ascending=True)
etab_annee=pd.merge(etab_annee[['EtablissementValideur_FR','rank']],df_valide[['EtablissementValideur_FR','Annee']],how='left',on=['EtablissementValideur_FR'])
etab_annee=etab_annee.value_counts().reset_index().sort_values('rank',ascending=False)
etab_annee['Annee']=etab_annee['Annee'].astype(str)

fig_etab_annee = px.bar(etab_annee.reset_index(), x="count", y="EtablissementValideur_FR",color='Annee', hover_data=['count'],barmode='group')
st.plotly_chart(fig_etab_annee)

st.header('Classement de la dépense effective par institution')
etab_depense=pd.DataFrame(df_valide[['EtablissementValideur_FR','APCRemise']])
etab_depense=etab_depense[(etab_depense['APCRemise'])!='']
etab_depense=etab_depense.groupby('EtablissementValideur_FR').sum()
etab_depense['rank']=etab_depense.rank(ascending=False,method='dense')
etab_depense=etab_depense.nsmallest(10,"rank").sort_values('APCRemise',ascending=True)

etab_depense=etab_depense.reset_index()
etab_depense=etab_depense[['EtablissementValideur_FR','APCRemise']]

fig_etab_depense = px.bar(etab_depense.reset_index(), x="APCRemise", y="EtablissementValideur_FR", hover_data=['APCRemise'])
st.plotly_chart(fig_etab_depense)



