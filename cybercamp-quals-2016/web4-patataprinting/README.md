# CyberCamp Quals 2016 - Web 4 - Patataprinting


En esta prueba nos encontramos con una página estática con un enlace al Token de la prueba, si accedemos a token.secret, nos devuelve un error 403.




Ante este punto muerto, después de probar cualquier cosa absurda que se nos ocurra y no obtener resultado pasamos a nuestra herramienta favorita de botón gordo… Nikto, dirb/wfuzz, Acunetix.

Aunque normalmente los CTF suelen estar diseñados para evitar que el uso de estas herramientas funcione, en las pruebas de SQL la herramienta SQLmap funcionaba perfectamente, así que no perdíamos nada por intentarlo.

En poco tiempo el crawler encuentra una jugosa carpeta llamada ‘phpmyadmin’, ya tenemos trabajo.

Una vez accedemos nos encontramos la aplicación phpmyadmin protegida por contraseña.



Probamos las contraseñas por defecto ‘root’:’root’, ‘root’:”, ‘admin’:’admin’ sin conseguir nada. Una vez le damos a cancelar observamos el siguiente mensaje indicándonos la versión de phpMyAdmin 3.0.0-pl9, una bastante antigua y posiblemente con alguna vulnerabilidad.



Lo primero es buscar que vulnerabilidades tiene esta versión, en un principio no encontramos nada refiriéndose a ‘pl9’, pero lo dejamos pasar y buscamos vulnerabilidades simplemente para la versión 3.0.0.

Rápidamente encontramos 3 vulns con exploit publicado, recordemos que esto es un CTF, y que raramente nos van a pedir que utilicemos una vulnerabilidad sin exploit publicado.

Un rato mas tarde, no ha funcionado ninguna de las 3 vulnerabilidades, incluso en la máquina algunos archivos directamente ni existen.

El siguiente paso es descargar esta versión de phpMyAdmin y analizar su contenido, a ver si podemos localizar que archivos se encuentran disponibles y utilizar el exploit adecuado a ello.



Sorpresa, las versiones antiguas ya no están disponibles!!

En este punto, procedo a descargar TODAS las versiones de phpMyAdmin, tanto de la web oficial, como de cualquier parte de internet donde se encuentren las versiones mas antiguas.

Una vez organizadas en mi ordenador, tenemos dos tareas, generar un wordlist para el fuzzer, y guardar el MD5 de todos los archivos.



Aunque seguramente hayan formas mas eficientes o bonitas, en ese momento recurrí al comando find y md5 del terminal de OSX.

El siguiente paso es lanzar el fuzzer, en mi caso utilizo dirsearch que funciona perfectamente en OSX.



Antes de seguir, os haré un pequeño spoiler, la versión no es 3.0.0-pl9, las autores de la prueba han jugado con nosotros :’(

Una vez conocemos que archivos están disponibles, los descargamos a nuestra maquina y calculamos la firma MD5 de aquellos que sean estáticos, descartando los que tengan extension .php

Ahora, solo tenemos que buscar coincidencias con la lista que elaboramos al principio.

grep ${md5} md5.txt



En este caso, después de probar diferentes archivos, damos con uno que nos reduce la busqueda a unas pocas posibles versiones.

Aunque en este momento podríamos probar exploits para estas versiones, no iba a parar estando tan cerca de la versión exacta.

La versión exacta la encontraremos analizando el archivo translators.html

Este archivo ha sido modificado cambiando el número de versión, así que su firma no nos sirve para identificarlo.

La diferencia mas evidente entre las versiones 2.6.4-pl1 y 2.6.4-pl2 es la eliminacion de las palabras so called. También hay otro detalle que nos hubiera ayudado a identificar la versión, la errata en la palabra developement



Una vez sabemos la version exacta, 2.6.4-pl1, solo nos queda encontrar un exploit que lanzarle.

Aunque en CVEdetails no aparece ningún exploit, se puede encontrar en exploitdb un exploit para la vulnerabilidad CVE-2005-3299.

Lanzamos el exploit….. y no funciona. Vemos que el exploit solo funciona por HTTP y puerto 80, nosotros necesitamos lanzarlo a una web HTTPS en un puerto poco común.

Mi solución rápida fue utilizar netcat nc -l 80 y lanzarme el exploit a mi mismo, de esta forma puedo ver la petición HTTP que realiza el exploit y replicarla con el Repeater de Burp, una vez lanzado se obteniene el archivo con el token localizado en ../../token.secret



PD: Las credenciales para acceder al phpMyAdmin eran el usuario admin con la contraseña en blanco, aunque al ser una cuenta sin privilegios no hubiera sido posible realizar consultas SQL.














<style type="text/css">.disclaimer{text-align:right;font-size:x-small}.banner{background-color:#fff;text-align:left}.cacheContent{position:relative}.b_vPanel>div{padding-bottom:10px}.b_vPanel>div:last-child{padding:0}.banner a{color:#001ba0}</style><base href="https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/" /><meta http-equiv="content-type" content="text/html; charset=utf-8" /><!-- Banner:Start --><!--LocalizedDate:15/05/2018--><!--InvariantDate:5/15/2018--><div class="banner"><div class="b_vPanel"><div><!-- Title:Start -->Has llegado a la p&#225;gina guardada en cach&#233; de <strong><a href="https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/" h="ID=SERP,5003.1">https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/</a></strong><!-- Title:End --></div><div><!-- Content:Start -->A continuaci&#243;n aparece una instant&#225;nea de la p&#225;gina web tal y como aparec&#237;a en <strong>15/05/2018</strong> (la &#250;ltima vez que nuestro rastreador la visit&#243;). Esta es la versi&#243;n de la p&#225;gina que se us&#243; para la clasificaci&#243;n de los resultados de b&#250;squeda. Puede que la p&#225;gina haya cambiado desde la &#250;ltima vez que la guardamos en cach&#233;. Para ver lo que puede haber cambiado (sin la informaci&#243;n destacada), <a href="https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/" h="ID=SERP,5003.2">ve a la p&#225;gina actual</a>.<!-- Content:End --></div><div><!-- Disclaimer:Start --><div class="disclaimer">Bing no se hace responsable del contenido de esta p&#225;gina.</div><!-- Disclaimer:End --></div><!-- Banner:End --></div></div><div class="cacheContent"><!doctype html>
<!--
  Minimal Mistakes Jekyll Theme 4.6.0 by Michael Rose
  Copyright 2017 Michael Rose - mademistakes.com | @mmistakes
  Free for personal and commercial use under the MIT license
  https://github.com/mmistakes/minimal-mistakes/blob/master/LICENSE.txt
-->
<html lang="es" class="no-js">
  <head>
    <meta charset="utf-8">

<!-- begin SEO -->









<title>CyberCamp Quals 2016 - Web 4 - Patataprinting - JesuX Blog</title>




<meta name="description" content="En esta prueba nos encontramos con una página estática con un enlace al Token de la prueba, si accedemos a token.secret, nos devuelve un error 403.">




<meta name="author" content="Jesus">

<meta property="og:locale" content="es">
<meta property="og:site_name" content="JesuX Blog">
<meta property="og:title" content="CyberCamp Quals 2016 - Web 4 - Patataprinting">


  <link rel="canonical" href="https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/">
  <meta property="og:url" content="https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/">



  <meta property="og:description" content="En esta prueba nos encontramos con una página estática con un enlace al Token de la prueba, si accedemos a token.secret, nos devuelve un error 403.">















  <meta name="twitter:site" content="@jesux">
  <meta name="twitter:title" content="CyberCamp Quals 2016 - Web 4 - Patataprinting">
  <meta name="twitter:description" content="En esta prueba nos encontramos con una página estática con un enlace al Token de la prueba, si accedemos a token.secret, nos devuelve un error 403.">
  <meta name="twitter:url" content="https://jesux.es/ctf-writeup/cybercamp-quals-2016-web-4-patataprinting/">

  
    <meta name="twitter:card" content="summary">
    
  

  
    <meta name="twitter:creator" content="@Jesus">
  







  <meta property="og:type" content="article">
  <meta property="article:published_time" content="2016-11-04T09:00:00+01:00">














<!-- end SEO -->


<link href="https://jesux.es/feed.xml" type="application/atom+xml" rel="alternate" title="JesuX Blog Feed">

<!-- http://t.co/dKP3o1e -->
<meta name="HandheldFriendly" content="True">
<meta name="MobileOptimized" content="320">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<script>
  document.documentElement.className = document.documentElement.className.replace(/\bno-js\b/g, '') + ' js ';
</script>

<!-- For all browsers -->
<link rel="stylesheet" href="https://jesux.es/assets/css/main.css">

<!--[if lte IE 9]>
  <style>
    /* old IE unsupported flexbox fixes */
    .greedy-nav .site-title {
      padding-right: 3em;
    }
    .greedy-nav button {
      position: absolute;
      top: 0;
      right: 0;
      height: 100%;
    }
  </style>
<![endif]-->


    <!-- start custom head snippets -->

<!-- insert favicons. use http://realfavicongenerator.net/ -->
<link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon/favicon-16x16.png">
<link rel="manifest" href="/assets/favicon/manifest.json">
<link rel="mask-icon" href="/assets/favicon/safari-pinned-tab.svg" color="#5bbad5">
<meta name="theme-color" content="#ffffff">

<!-- end custom head snippets -->
  </head>

  <body class="layout--single">

    <!--[if lt IE 9]>
<div class="notice--danger align-center" style="margin: 0;">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</div>
<![endif]-->
    <div class="masthead">
  <div class="masthead__inner-wrap">
    <div class="masthead__menu">
      <nav id="site-nav" class="greedy-nav">
        <a class="site-title" href="https://jesux.es/">JesuX Blog</a>
        <ul class="visible-links">
          
        </ul>
        <button type="button">
          <span class="visually-hidden">Toggle Menu</span>
          <div class="navicon"></div>
        </button>
        <ul class="hidden-links hidden"></ul>
      </nav>
    </div>
  </div>
</div>

    



<div id="main" role="main">
  
  <div class="sidebar sticky">
  

<div itemscope itemtype="http://schema.org/Person">

  
    <div class="author__avatar">
      
        <img src="https://jesux.es/assets/img/logo.jpg" class="author__avatar" alt="Jesus" itemprop="image">
      
    </div>
  

  <div class="author__content">
    <h3 class="author__name" itemprop="name">Jesus</h3>
    
      <p class="author__bio" itemprop="description">
        I am an amazing patata.
      </p>
    
  </div>

  <div class="author__urls-wrapper">
    <button class="btn btn--inverse">Seguir</button>
    <ul class="author__urls social-icons">
      
        <li itemprop="homeLocation" itemscope itemtype="http://schema.org/Place">
          <i class="fa fa-fw fa-map-marker" aria-hidden="true"></i> <span itemprop="name">Spain</span>
        </li>
      

      

      
        <li>
          <a href="mailto:blog@jesux.es">
            <meta itemprop="email" content="blog@jesux.es" />
            <i class="fa fa-fw fa-envelope-square" aria-hidden="true"></i> Email
          </a>
        </li>
      

      

      
        <li>
          <a href="https://twitter.com/HackingPatatas" itemprop="sameAs">
            <i class="fa fa-fw fa-twitter-square" aria-hidden="true"></i> Twitter
          </a>
        </li>
      

      

      

      

      

      

      

      

      
        <li>
          <a href="https://github.com/jesux" itemprop="sameAs">
            <i class="fa fa-fw fa-github" aria-hidden="true"></i> GitHub
          </a>
        </li>
      

      

      

      

      

      

      

      

      

      

      

      

      

      

      <!--
  <li>
    <a href="http://link-to-whatever-social-network.com/user/" itemprop="sameAs">
      <i class="fa fa-fw" aria-hidden="true"></i> Custom Social Profile Link
    </a>
  </li>
-->
    </ul>
  </div>
</div>

  
  </div>


  <article class="page" itemscope itemtype="http://schema.org/CreativeWork">
    <meta itemprop="headline" content="CyberCamp Quals 2016 - Web 4 - Patataprinting">
    <meta itemprop="description" content="En esta prueba nos encontramos con una página estática con un enlace al Token de la prueba, si accedemos a token.secret, nos devuelve un error 403.">
    <meta itemprop="datePublished" content="November 04, 2016">
    

    <div class="page__inner-wrap">
      
        <header>
          <h1 class="page__title" itemprop="headline">CyberCamp Quals 2016 - Web 4 - Patataprinting
</h1>
          
        </header>
      

      <section class="page__content" itemprop="text">
        
        <p>En esta prueba nos encontramos con una página estática con un enlace al Token de la prueba, si accedemos a <strong>token.secret</strong>, nos devuelve un error 403.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/web4-index-1024x746.png" alt="" /></p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/web4-token403-1024x746.png" alt="" /></p>

<p>Ante este punto muerto, después de probar cualquier cosa absurda que se nos ocurra y no obtener resultado pasamos a nuestra herramienta favorita de botón gordo… Nikto, dirb/wfuzz, Acunetix.</p>

<p>Aunque normalmente los CTF suelen estar diseñados para evitar que el uso de estas herramientas funcione, en las pruebas de SQL la herramienta SQLmap funcionaba perfectamente, así que no perdíamos nada por intentarlo.</p>

<p>En poco tiempo el crawler encuentra una jugosa carpeta llamada ‘phpmyadmin’, ya tenemos trabajo.</p>

<p>Una vez accedemos nos encontramos la aplicación phpmyadmin protegida por contraseña.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-phpmyadmin-login-1024x798.png" alt="" /></p>

<p>Probamos las contraseñas por defecto ‘root’:’root’, ‘root’:”, ‘admin’:’admin’ sin conseguir nada. Una vez le damos a cancelar observamos el siguiente mensaje indicándonos la versión de phpMyAdmin 3.0.0-pl9, una bastante antigua y posiblemente con alguna vulnerabilidad.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-phpmyadmin-version.png" alt="" /></p>

<p>Lo primero es buscar que vulnerabilidades tiene esta versión, en un principio no encontramos nada refiriéndose a ‘pl9’, pero lo dejamos pasar y buscamos vulnerabilidades simplemente para la versión 3.0.0.</p>

<p>Rápidamente encontramos 3 vulns con exploit publicado, recordemos que esto es un CTF, y que raramente nos van a pedir que utilicemos una vulnerabilidad sin exploit publicado.</p>

<p>Un rato mas tarde, no ha funcionado ninguna de las 3 vulnerabilidades, incluso en la máquina algunos archivos directamente ni existen.</p>

<p>El siguiente paso es descargar esta versión de phpMyAdmin y analizar su contenido, a ver si podemos localizar que archivos se encuentran disponibles y utilizar el exploit adecuado a ello.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-phpmyadmin-nodisp-1024x227.png" alt="" /></p>

<p>Sorpresa, las versiones antiguas ya no están disponibles!!</p>

<p>En este punto, procedo a descargar TODAS las versiones de phpMyAdmin, tanto de la web oficial, como de cualquier parte de internet donde se encuentren las versiones mas antiguas.</p>

<p>Una vez organizadas en mi ordenador, tenemos dos tareas, generar un wordlist para el fuzzer, y guardar el MD5 de todos los archivos.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-phpmyadmin-versiones.png" alt="" /></p>

<p>Aunque seguramente hayan formas mas eficientes o bonitas, en ese momento recurrí al comando find y md5 del terminal de OSX.</p>

<p>El siguiente paso es lanzar el fuzzer, en mi caso utilizo <a href="https://github.com/maurosoria/dirsearch">dirsearch</a> que funciona perfectamente en OSX.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-dirsearch-1024x696.png" alt="" /></p>

<p>Antes de seguir, os haré un pequeño spoiler, la versión no es 3.0.0-pl9, las autores de la prueba han jugado con nosotros :’(</p>

<p>Una vez conocemos que archivos están disponibles, los descargamos a nuestra maquina y calculamos la firma MD5 de aquellos que sean estáticos, descartando los que tengan extension .php</p>

<p>Ahora, solo tenemos que buscar coincidencias con la lista que elaboramos al principio.</p>

<p><code class="highlighter-rouge">grep ${md5} md5.txt</code></p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-md5-upgrade-1-1024x109.png" alt="" /></p>

<p>En este caso, después de probar diferentes archivos, damos con uno que nos reduce la busqueda a unas pocas posibles versiones.</p>

<p>Aunque en este momento podríamos probar exploits para estas versiones, no iba a parar estando tan cerca de la versión exacta.</p>

<p>La versión exacta la encontraremos analizando el archivo <em>translators.html</em></p>

<p>Este archivo ha sido modificado cambiando el número de versión, así que su firma no nos sirve para identificarlo.</p>

<p>La diferencia mas evidente entre las versiones 2.6.4-pl1 y 2.6.4-pl2 es la eliminacion de las palabras so called. También hay otro detalle que nos hubiera ayudado a identificar la versión, la errata en la palabra <em>developement</em></p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/Web4-translators-1024x331.png" alt="" /></p>

<p>Una vez sabemos la version exacta, 2.6.4-pl1, solo nos queda encontrar un exploit que lanzarle.</p>

<p>Aunque en CVEdetails no aparece ningún exploit, se puede encontrar en exploitdb un <a href="https://www.exploit-db.com/exploits/1244/">exploit para la vulnerabilidad CVE-2005-3299</a>.</p>

<p>Lanzamos el exploit….. y no funciona. Vemos que el exploit solo funciona por HTTP y puerto 80, nosotros necesitamos lanzarlo a una web HTTPS en un puerto poco común.</p>

<p>Mi solución rápida fue utilizar netcat <code class="highlighter-rouge">nc -l 80</code> y lanzarme el exploit a mi mismo, de esta forma puedo ver la petición HTTP que realiza el exploit y replicarla con el Repeater de Burp, una vez lanzado se obteniene el archivo con el token localizado en <em>../../token.secret</em></p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-solucion-1024x190.png" alt="" /></p>

<p>PD: Las credenciales para acceder al phpMyAdmin eran el usuario admin con la contraseña en blanco, aunque al ser una cuenta sin privilegios no hubiera sido posible realizar consultas SQL.</p>

<p><img src="/assets/img/cybercamp-quals-2016-web-4-patataprinting/WEB4-phpmyadmin-1024x798.png" alt="" /></p>

        
      </section>

      <footer class="page__meta">
        
        
  


  
  
  

  <p class="page__taxonomy">
    <strong><i class="fa fa-fw fa-tags" aria-hidden="true"></i> Etiquetas: </strong>
    <span itemprop="keywords">
    
      
      
      <a href="https://jesux.es/tags/#ctf" class="page__taxonomy-item" rel="tag">CTF</a><span class="sep">, </span>
    
      
      
      <a href="https://jesux.es/tags/#cybercamp2016" class="page__taxonomy-item" rel="tag">CyberCamp2016</a><span class="sep">, </span>
    
      
      
      <a href="https://jesux.es/tags/#phpmyadmin" class="page__taxonomy-item" rel="tag">phpMyAdmin</a>
    
    </span>
  </p>




  


  
  
  

  <p class="page__taxonomy">
    <strong><i class="fa fa-fw fa-folder-open" aria-hidden="true"></i> Categorías: </strong>
    <span itemprop="keywords">
    
      
      
      <a href="https://jesux.es/categories/#ctf-writeup" class="page__taxonomy-item" rel="tag">CTF-Writeup</a>
    
    </span>
  </p>


        
          <p class="page__date"><strong><i class="fa fa-fw fa-calendar" aria-hidden="true"></i> Actualizado:</strong> <time datetime="2016-11-04T09:00:00+01:00">November 04, 2016</time></p>
        
      </footer>

      

    </div>

    
  </article>

  
  
</div>


    <div class="page__footer">
      <footer>
        <!-- start custom footer snippets -->

<!-- end custom footer snippets -->
        <div class="page__footer-follow">
  <ul class="social-icons">
    
      <li><strong>Seguir:</strong></li>
    
    
      <li><a href="https://twitter.com/jesux"><i class="fa fa-fw fa-twitter-square" aria-hidden="true"></i> Twitter</a></li>
    
    
    
      <li><a href="http://github.com/jesux"><i class="fa fa-fw fa-github" aria-hidden="true"></i> GitHub</a></li>
    
    
    
    <li><a href="https://jesux.es/feed.xml"><i class="fa fa-fw fa-rss-square" aria-hidden="true"></i> Feed</a></li>
  </ul>
</div>

<div class="page__footer-copyright">&copy; 2018 Jesus. Powered by <a href="http://jekyllrb.com" rel="nofollow">Jekyll</a> &amp; <a href="https://mademistakes.com/work/minimal-mistakes-jekyll-theme/" rel="nofollow">Minimal Mistakes</a>.</div>

      </footer>
    </div>

    
  <script src="https://jesux.es/assets/js/main.min.js"></script>






  </body>
</html></div>