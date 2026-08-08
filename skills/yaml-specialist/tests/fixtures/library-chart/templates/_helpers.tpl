{{- define "yaml-specialist-library-fixture.message" -}}
message: {{ .Values.library.message | quote }}
{{- end -}}
