# We'll use a dataframe for convenience, sorting etc
explanation_client = pd.DataFrame({'shap_value': response_api_explain.json().values(),
                                       'feature_name': response_api_explain.json().keys()})

 # Getting most important lines using absolute values
explanation_client['shap_value_abs'] = explanation_client.shap_value.map(abs)
# Tagging positive and negative values and setting a color for plotting
explanation_client['color'] = explanation_client.shap_value > 0
explanation_client.color.replace(True, 'red', inplace=True)
explanation_client.color.replace(False, 'green', inplace=True)
# Sorting by abs value
explanation_client.sort_values('shap_value_abs', ascending=False, inplace=True)
# Getting only the number asked by user
explanation_client = explanation_client.head(nb_features_explain)
# Changing the order because plotly plots from bottom to top
explanation_client.sort_values('shap_value_abs', ascending=True, inplace=True)
# Getting raw data and writing it on the labels
explanation_client['raw_data'] = data_raw_client[explanation_client.feature_name].iloc[0].values
explanation_client['bar_labels'] = explanation_client.feature_name + '\n=' \
                                       + explanation_client.raw_data.round(2).astype(str)
# Setup figure
fig = go.Figure(go.Bar(x=explanation_client['shap_value'],
                           y=explanation_client['bar_labels'],
                           orientation='h',
                           marker={'color': explanation_client['color']},
                           ),
                    )
fig.update_layout(xaxis_title="Influence sur le niveau de risque",
                      )

st.plotly_chart(fig,
                    use_container_width=True)