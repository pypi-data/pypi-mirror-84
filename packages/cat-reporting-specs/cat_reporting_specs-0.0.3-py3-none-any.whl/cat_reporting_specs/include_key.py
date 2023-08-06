
INCLUDE_KEY = {
    'Required': 'R',    # Required for the given event. This field must always be included.
    'Conditional': 'C', # Conditionally required for the given event, depending upon other values submitted in the Reportable Event message.
    'Optional': 'O',    # Optional for the given event. May be included at the discretion of the reporter/submitter.
    'ATS': 'A',         # Applicable for ATSs only. Required when the CAT Reporter IMID is an ATS.
}
