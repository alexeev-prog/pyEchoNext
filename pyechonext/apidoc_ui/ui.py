class APIDocUI:
	"""
	This class describes an api document ui.
	"""

	def __init__(self, specification: dict):
		"""
		Constructs a new instance.

		:param		specification:	The specification
		:type		specification:	dict
		"""
		self.specification = specification

	def generate_section(
		self,
		route: str,
		summary_get: str,
		summary_post: str,
		get_responses: dict,
		post_responses: dict,
	) -> str:
		"""
		generate section

		:param		route:			 The route
		:type		route:			 str
		:param		summary_get:	 The summary get
		:type		summary_get:	 str
		:param		summary_post:	 The summary post
		:type		summary_post:	 str
		:param		get_responses:	 The get responses
		:type		get_responses:	 dict
		:param		post_responses:	 The post responses
		:type		post_responses:	 dict

		:returns:	template section
		:rtype:		str
		"""

		template = f"""
<div class="section">
		<div class="section-header">
			<span>{route}</span>
			<span class="collapse-icon">➡️</span>
		</div>
		<div class="section-content">
			<div class="method">
				<strong>GET</strong>
				<p>{summary_get}</p>
				<div class="responses">
					{"".join([f"<div class='response-item'>{key}: {value["description"]}.</div>" for key, value in get_responses.items()])}
				</div>
			</div>
			<div class="method">
				<strong>POST</strong>
				<p>{summary_post}</p>
				<div class="responses">
					<div class="responses">
					{"".join([f"<div class='response-item'>{key}: {value["description"]}.</div>" for key, value in post_responses.items()])}
				</div>
				</div>
			</div>
		</div>
	</div>
				   """

		return template

	def generate_html_page(self) -> str:
		"""
		Generate html page template

		:returns:	template
		:rtype:		str
		"""
		template = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>API Documentation</title>
	<style>
		body {
			font-family: Arial, sans-serif;
			margin: 0;
			padding: 0;
			background-color: #f9f9f9;
			color: #333;
		}
		h1, h2, h3 {
			margin: 0;
			padding: 10px 0;
		}
		.container {
			max-width: 800px;
			margin: 40px auto;
			padding: 20px;
			background: #fff;
			border-radius: 8px;
			box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
		}
		.version {
			font-size: 14px;
			color: #555;
			margin-bottom: 20px;
		}
		.info-section {
			border-bottom: 1px solid #ddd;
			padding-bottom: 20px;
			margin-bottom: 20px;
		}
		.section {
			border-radius: 5px;
			overflow: hidden;
			margin-bottom: 20px;
			transition: box-shadow 0.3s ease;
		}
		.section-header {
			padding: 15px;
			background: #007bff;
			color: white;
			cursor: pointer;
			position: relative;
			font-weight: bold;
			display: flex;
			justify-content: space-between;
			align-items: center;
		}
		.section-content {
			padding: 15px;
			display: none;
			overflow: hidden;
			background-color: #f1f1f1;
		}
		.method {
			border-bottom: 1px solid #ddd;
			padding: 10px 0;
		}
		.method:last-child {
			border-bottom: none;
		}
		.responses {
			margin-top: 10px;
			padding-left: 15px;
			font-size: 14px;
			color: #555;
		}
		.response-item {
			margin-bottom: 5px;
		}
		.collapse-icon {
			transition: transform 0.3s;
		}
		.collapse-icon.collapsed {
			transform: rotate(90deg);
		}
		.section:hover {
			box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
		}
	</style>
</head>
<body>

<div class="container">
	<h1>OpenAPI Documentation</h1>
	<h2>PyEchoNext Web Application</h2>
	<div class="version">OpenAPI Version: {{openapi-version}}</div>
	<div class="info-section">
		<h2>Application Information</h2>
		<p><strong>Title:</strong> {{info_title}}</p>
		<p><strong>Version:</strong> {{info_version}}</p>
		<p><strong>Description:</strong> {{info_description}}</p>
	</div>

	{{sections}}

<script>
	document.querySelectorAll('.section-header').forEach(header => {
		header.addEventListener('click', () => {
			const content = header.nextElementSibling;
			const icon = header.querySelector('.collapse-icon');

			if (content.style.display === "block") {
				content.style.display = "none";
				icon.classList.add('collapsed');
			} else {
				content.style.display = "block";
				icon.classList.remove('collapsed');
			}
		});
	});
</script>

</body>
</html>
				   """

		content = {
			"{{openapi-version}}": self.specification["openapi"],
			"{{info_title}}": self.specification["info"]["title"],
			"{{info_version}}": self.specification["info"]["version"],
			"{{info_description}}": self.specification["info"]["description"],
			"{{sections}}": "\n".join(
				[
					self.generate_section(
						path,
						value["get"]["summary"],
						value["post"]["summary"],
						value["get"]["responses"],
						value["post"]["responses"],
					)
					for path, value in self.specification["paths"].items()
				]
			),
		}

		for key, value in content.items():
			template = template.replace(key, value)

		return template
