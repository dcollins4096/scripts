<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:cadac="http://cadac.sdsc.edu/schema">

  <xsl:output method="xml" version="1.0" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" indent="yes"/>
  <xsl:template match="/">

    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Computational Astrophysics Data Analysis Center</title>
	<link rel="stylesheet" type="text/css" href="/css/cadac.css" media="all" />
	<link rel="stylesheet" type="text/css" href="/css/print.css" media="print" />
      </head>

      <body>
	<div id="sidebar"></div>
	<div id="content">
	  <h1>CADAC</h1>
	  <div id="help_link">
	    <a href="help.html">help</a>
	  </div>

	  <div id="navcontainer">
	    <ul id="navlist">
	      <li class="page_item">
		<a href="index.html" class="selected" title="Project Home / Index">Home</a>
	      </li>
	      <li class="page_item">
		<a href="about.html"  >About</a>
	      </li>
	      <li>
		<a href="/cadac/members">Members</a>
	      </li>
              <li>
		<a href="doc/index.html" >Documentation</a>
	      </li>

	    </ul>
	  </div>

	  <xsl:apply-templates />

	</div>

	<div id="footer">

	  <p >
	    <a class="logo" id="sdsclogo" href="http://www.sdsc.edu/">
	      <img src="/images/sdsc-red.jpg" alt="San Diego Supercomputer Center" />
	    </a>
	    <a class="logo" id="ucsdlogo" href="http://www.ucsd.edu/">
	      <img src="/images/logo_ucsd.gif" alt="Official web page of the University of California, San Diego" />
	    </a>

	    <a class="logo" id="lcalogo" href="http://lca.ucsd.edu/">
	      <img src="/images/lcalogo_sm.png" alt="Laboratory for Computational Astrophysics" />
	    </a>
	  </p>

	  <p class="legalese">
	    <a href="http://www.ucsd.edu/">  Official web page of the University of California, San Diego.</a>
	  </p>
	</div>

      </body>
    </html>
  </xsl:template>

  <xsl:template match="cadac:RunList" xmlns="http://www.w3.org/1999/xhtml">
    <table>
      <xsl:for-each select="cadac:Run">
	<tr>
	  <td><a href="{cadac:id}">More</a></td>
	  <td><xsl:value-of select="cadac:Successful" /></td>
	  <td><xsl:value-of select="cadac:Name" /></td>
	  <td><xsl:value-of select="cadac:Computer" /></td>
	  <td><xsl:value-of select="cadac:Program" /></td>

	  <td><xsl:value-of select="cadac:Nodes" /></td>
	  <td><xsl:value-of select="cadac:TasksPerNode" /></td>

	  <td><xsl:value-of select="cadac:JobID" /></td>
	  <td><xsl:value-of select="cadac:JobName" /></td>

	  <td><xsl:value-of select="cadac:SubmitTime" /></td>
	  <td><xsl:value-of select="cadac:StartTime" /></td>
	  <td><xsl:value-of select="cadac:EndTime" /></td> 
	</tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="cadac:Run" xmlns="http://www.w3.org/1999/xhtml">
    <ul>
      <li><xsl:value-of select="cadac:Successful" /></li>
      <li><xsl:value-of select="cadac:Name" /></li>
      <li><xsl:value-of select="cadac:Computer" /></li>
      <li><xsl:value-of select="cadac:Program" /></li>

      <li><xsl:value-of select="cadac:Nodes" /></li>
      <li><xsl:value-of select="cadac:TasksPerNode" /></li>

      <li><xsl:value-of select="cadac:JobID" /></li>
      <li><xsl:value-of select="cadac:JobName" /></li>

      <li><xsl:value-of select="cadac:SubmitTime" /></li>
      <li><xsl:value-of select="cadac:StartTime" /></li>
      <li><xsl:value-of select="cadac:EndTime" /></li> 
      <td><a href="./{cadac:id}/tags">Tags</a></td>
    </ul>
  </xsl:template>

  <xsl:template match="cadac:TagList" xmlns="http://www.w3.org/1999/xhtml">
    <ul>
      <xsl:for-each select="cadac:Tag">
	<li><a href="/cadac/members/{cadac:UserName}/{.}/runs/"><xsl:value-of select="." /></a></li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template match="cadac:MemberList" xmlns="http://www.w3.org/1999/xhtml">
    <table>
      <xsl:for-each select="cadac:Member">
	<tr>
	  <td><xsl:value-of select="cadac:UserName" /></td>
	  <td><xsl:value-of select="cadac:Name" /></td>
	  <td><a href="{cadac:PersonalSite}"><xsl:value-of select="cadac:Name" /></a></td>
	  <td><a href="/cadac/members/{cadac:UserName}">Member Info</a></td>
	</tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="cadac:Member" xmlns="http://www.w3.org/1999/xhtml">
    <h2><xsl:value-of select="cadac:Name" /></h2>

    <dl>
      <dt>CADAC User Name</dt>
      <dd><xsl:value-of select="cadac:UserName" /></dd>
      <dt>Personal Site</dt>
      <dd><a href="{cadac:PersonalSite}"><xsl:value-of select="cadac:PersonalSite" /></a></dd>
    </dl>
    <h3>All Runs</h3>
    <p><a href="/cadac/members/{cadac:UserName}/runs/">Runs</a></p>
    <h3>Runs by Tag</h3>
    <xsl:variable name="userName">
      <xsl:value-of select="cadac:UserName"/>
    </xsl:variable> 
    <ul>
      <xsl:for-each select="//cadac:Tag">
	<li><a href="/cadac/members/{$userName}/{.}/runs/"><xsl:value-of select="." /></a></li>
      </xsl:for-each>
    </ul>

  </xsl:template>

</xsl:stylesheet>
