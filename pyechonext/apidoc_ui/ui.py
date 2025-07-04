import json

from pyechonext.response import Response


class APIDocUI:
    """
    This class describes an api document ui.
    """

    def __init__(self, specification: dict):
        """
        Constructs a new instance.

        :param			specification:	  The specification
        :type		  specification:	   dict
        """
        self.specification = specification

    def generate_section(
        self,
        route: str,
        summary_get: str,
        summary_post: str,
        get_responses: dict,
        post_responses: dict,
        value: dict,
    ) -> str:
        """
        generate section

        :param			route:			   The route
        :type		  route:				str
        :param			summary_get:	   The summary get
        :type		  summary_get:		str
        :param			summary_post:		 The summary post
        :type		  summary_post:		  str
        :param			get_responses:	   The get responses
        :type		  get_responses:		dict
        :param			post_responses:		 The post responses
        :type		  post_responses:	  dict

        :returns:	  template section
        :rtype:			  str
        """

        template = f"""
<div class="section">
		<div class="section-header">
			<span>{route}</span>
			<span class="collapse-icon">➡️</span>
		</div>
		<div class="section-content">
			<pre><code class="language-json">{json.dumps(value, indent=2)}</code></pre>
			<div class="method">
				<strong>GET</strong>
				<p class='summary'>{summary_get}</p>
				
				<div class="responses">
					{"".join([f"<div class='response-item'><span class='span-key'>{key}</span>: {value['description']}.</div>" for key, value in get_responses.items()])}
				</div>
			</div>
			<div class="method">
				<strong>POST</strong>
				<p class='summary'>{summary_post}</p>
				<div class="responses">
					<div class="responses">
					{"".join([f"<div class='response-item'><span class='span-key'>{key}</span>: {value['description']}.</div>" for key, value in post_responses.items()])}
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

        :returns:	  template
        :rtype:			  str
        """
        template = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>API Documentation</title>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
	<style>

		body {
			font-family: Arial, sans-serif;
			margin: 0;
			padding: 0;
			background-color: #f3f3f3;
			color: #333;
			display: block;
  overflow-x: auto;
		}
		.span-key {
			font-size: 15px;
			color: #007bff;
		}
		h1, h2, h3 {
			margin: 0;
			padding: 10px 0;
		}
		pre {
		
			margin-bottom: 10px;
  padding: 5px;
			font-family: monospace;
			margin: 10px;
			padding: 10px;
			white-space: pre-wrap;			 /* Since CSS 2.1 */
			white-space: -moz-pre-wrap;		   /* Mozilla, since 1999 */
			white-space: -pre-wrap;			   /* Opera 4-6 */
			white-space: -o-pre-wrap;	   /* Opera 7 */
			word-wrap: break-word;			 /* Internet Explorer 5.5+ */
		}
		code{
		border-radius: 5px;
}
		.summary {
			border-radius: 4px;
			box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
			color: #222222;
			padding: 10px;
			border-left: 2px solid #007bff;
		}
		.container {
			max-width: 1000px;
			margin: 20px auto;
			padding: 20px;
			border: 1px solid #007bff3;
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
			transition: box-shadow 0.3s ease;
		}
		.section-header {
			margin-bottom: 10px;
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
			margin-bottom: 10px;
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
			transform: rotate(90deg);
		}
		.collapse-icon.collapsed {
			transform: rotate(0deg);
		}
		pre code.hljs {
  display: block;
  overflow-x: auto;
  padding: 1em
}
code.hljs {
  padding: 3px 5px
}
/*

Atom One Light by Daniel Gamage
Original One Light Syntax theme from https://github.com/atom/one-light-syntax

base:	   #fafafa
mono-1:		   #383a42
mono-2:		   #686b77
mono-3:		   #a0a1a7
hue-1:		 #0184bb
hue-2:		 #4078f2
hue-3:		 #a626a4
hue-4:		 #50a14f
hue-5:		 #e45649
hue-5-2: #c91243
hue-6:		 #986801
hue-6-2: #c18401

*/
.hljs {
  color: #383a42;
  background: #fafafa
}
.hljs-comment,
.hljs-quote {
  color: #a0a1a7;
  font-style: italic
}
.hljs-doctag,
.hljs-keyword,
.hljs-formula {
  color: #a626a4
}
.hljs-section,
.hljs-name,
.hljs-selector-tag,
.hljs-deletion,
.hljs-subst {
  color: #e45649
}
.hljs-literal {
  color: #0184bb
}
.hljs-string,
.hljs-regexp,
.hljs-addition,
.hljs-attribute,
.hljs-meta .hljs-string {
  color: #50a14f
}
.hljs-attr,
.hljs-variable,
.hljs-template-variable,
.hljs-type,
.hljs-selector-class,
.hljs-selector-attr,
.hljs-selector-pseudo,
.hljs-number {
  color: #986801
}
.hljs-symbol,
.hljs-bullet,
.hljs-link,
.hljs-meta,
.hljs-selector-id,
.hljs-title {
  color: #4078f2
}
.hljs-built_in,
.hljs-title.class_,
.hljs-class .hljs-title {
  color: #c18401
}
.hljs-emphasis {
  font-style: italic
}
.hljs-strong {
  font-weight: bold
}
.hljs-link {
  text-decoration: underline
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

	<br>
	<hr>
	<br>

	<h2>Full specification</h2>
	<pre><code class="language-json">{{spec}}</code></pre>

<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"></script>

<script>hljs.highlightAll();</script>

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

	document.addEventListener('DOMContentLoaded', (event) => {
		document.querySelectorAll('pre code').forEach((el) => {
			hljs.highlightElement(el);
		});
	});
</script>

</body>
</html>
				   """

        content = {
            "{{openapi-version}}": self.specification["openapi"],
            "{{spec}}": json.dumps(self.specification, indent=2),
            "{{info_title}}": self.specification["info"]["title"],
            "{{info_version}}": self.specification["info"]["version"],
            "{{info_description}}": self.specification["info"]["description"],
            "{{sections}}": "\n".join([
                self.generate_section(
                    path,
                    value["get"]["summary"],
                    value["post"]["summary"],
                    value["get"]["responses"],
                    value["post"]["responses"],
                    value,
                )
                for path, value in self.specification["paths"].items()
            ]),
        }

        for key, value in content.items():
            template = template.replace(key, value)

        return Response(body=template)
