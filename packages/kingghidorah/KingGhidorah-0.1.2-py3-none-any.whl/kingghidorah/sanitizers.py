def _url_sanitizer(url):
  # Check first character
  if url[0] == "/":
    url = url[1:]

  if "icontains" in url:
    return url

  # Check last character
  if url[-1] != "/":
    url = url + "/"

  # Check for format
  if url[-12:] == "?format=json":
    return url
  else:
    return url + "?format=json"
