import app_config

app = app_config.AppConfig()
print(app.get_location_config())
print(app.get_param("port"))
app.set_param("port","777")
print(app.get_param("port"))