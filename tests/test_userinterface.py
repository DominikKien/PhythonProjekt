# .coveragerc

[run]
# Verzeichnisse und Dateien, die von der Coverage-Messung ausgeschlossen werden sollen
omit =
    tests/*
    */__init__.py
    */migrations/*
    */venv/*
    */env/*
    */.venv/*
    */.env/*

# Quellverzeichnisse, auf die die Coverage angewendet wird
source =
    dein_paket_name  # Ersetze dies mit dem tatsächlichen Namen deines Pakets

branch = True
parallel = True

[report]
# Zeilen, die von der Coverage-Berichterstattung ausgeschlossen werden
exclude_lines =
    # Deaktivieren der Standard-Pragma
    pragma: no cover

    # Keine Warnungen für fehlende Debugging-Codezeilen
    def __repr__
    if self\.debug

    # Keine Warnungen, wenn Tests bestimmte Codezeilen nicht abdecken
    raise NotImplementedError
    if TYPE_CHECKING:

# Berichtseinstellungen
show_missing = True
skip_covered = True
precision = 2

[html]
# Einstellungen für den HTML-Bericht
directory = coverage_html_report

[xml]
# Einstellungen für den XML-Bericht
output = coverage.xml