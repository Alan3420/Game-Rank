<template>
  <div class="terminos-page">

    <!-- Hero -->
    <div class="terminos-hero">
      <div class="terminos-hero-inner">
        <span class="terminos-eyebrow">
          <i class="pi pi-shield"></i>
          Legal
        </span>
        <h1>Términos y Condiciones</h1>
        <p>Última actualización: 15 de mayo de 2026</p>
      </div>
    </div>

    <div class="terminos-layout">

      <!-- TOC lateral -->
      <aside class="terminos-toc">
        <p class="toc-title">Contenido</p>
        <nav>
          <a
            v-for="seccion in secciones"
            :key="seccion.id"
            :href="'#' + seccion.id"
            class="toc-link"
            :class="{ 'is-active': seccionActiva === seccion.id }"
            @click.prevent="scrollTo(seccion.id)"
          >
            <span class="toc-num">{{ seccion.num }}</span>
            {{ seccion.titulo }}
          </a>
        </nav>
      </aside>

      <!-- Contenido -->
      <article class="terminos-content">

        <section id="aceptacion" class="terminos-section">
          <div class="section-num">01</div>
          <h2>Aceptación de los Términos</h2>
          <p>
            Al acceder o utilizar Game Rank (en adelante, "la Plataforma"), aceptas quedar vinculado por los presentes
            Términos y Condiciones, así como por nuestra Política de Privacidad. Si no estás de acuerdo con alguna
            de estas disposiciones, te rogamos que no hagas uso de la Plataforma.
          </p>
          <p>
            Estos términos se aplican a todos los visitantes, usuarios registrados y cualquier persona que acceda
            o utilice los servicios ofrecidos por Game Rank.
          </p>
        </section>

        <section id="descripcion" class="terminos-section">
          <div class="section-num">02</div>
          <h2>Descripción del Servicio</h2>
          <p>
            Game Rank es una plataforma dedicada a la catalogación, valoración y descubrimiento de videojuegos.
            Los servicios que ofrecemos incluyen, entre otros:
          </p>
          <ul class="terminos-list">
            <li>Exploración de un catálogo extenso de videojuegos con información detallada.</li>
            <li>Sistema de puntuaciones y reseñas elaboradas por la comunidad de usuarios.</li>
            <li>Gestión de colecciones personales y listas de favoritos.</li>
            <li>Seguimiento del estado de juego (jugando, completado, pendiente, abandonado, deseado).</li>
            <li>Información sobre próximos lanzamientos de la industria.</li>
          </ul>
          <p>
            La información sobre videojuegos es obtenida a través de la API de RAWG (rawg.io), un servicio
            externo sobre el cual Game Rank no tiene control editorial. Nos reservamos el derecho de ampliar,
            modificar o descontinuar cualquiera de estos servicios en cualquier momento.
          </p>
        </section>

        <section id="cuenta" class="terminos-section">
          <div class="section-num">03</div>
          <h2>Registro y Cuenta de Usuario</h2>
          <p>
            Para acceder a las funcionalidades completas de Game Rank es necesario crear una cuenta. Al hacerlo,
            te comprometes a:
          </p>
          <ul class="terminos-list">
            <li>Proporcionar información veraz, completa y actualizada durante el registro.</li>
            <li>Mantener la confidencialidad de tus credenciales de acceso (correo electrónico y contraseña).</li>
            <li>Notificarnos inmediatamente ante cualquier uso no autorizado de tu cuenta.</li>
            <li>Ser el único responsable de todas las actividades realizadas bajo tu cuenta.</li>
            <li>No ceder, transferir ni compartir el acceso a tu cuenta con terceros.</li>
          </ul>
          <p>
            Game Rank se reserva el derecho de suspender o eliminar cuentas que infrinjan estos términos,
            sin previo aviso y sin obligación de reembolso de ningún tipo.
          </p>
        </section>

        <section id="uso-aceptable" class="terminos-section">
          <div class="section-num">04</div>
          <h2>Uso Aceptable</h2>
          <p>
            Al utilizar Game Rank, te comprometes a no llevar a cabo ninguna de las siguientes conductas:
          </p>
          <ul class="terminos-list">
            <li>Publicar contenido falso, engañoso, difamatorio, obsceno, ofensivo o que infrinja derechos de terceros.</li>
            <li>Acosar, amenazar o intimidar a otros usuarios de la Plataforma.</li>
            <li>Intentar acceder de forma no autorizada a sistemas, cuentas o datos de la Plataforma.</li>
            <li>Utilizar bots, scrapers u otras herramientas automatizadas para extraer contenido de Game Rank.</li>
            <li>Interferir o interrumpir la integridad o el rendimiento de la Plataforma.</li>
            <li>Publicar spam, publicidad no solicitada o contenido repetitivo de forma masiva.</li>
            <li>Suplantar la identidad de otra persona o entidad.</li>
            <li>Realizar cualquier actividad que infrinja la legislación aplicable.</li>
          </ul>
        </section>

        <section id="contenido" class="terminos-section">
          <div class="section-num">05</div>
          <h2>Contenido del Usuario</h2>
          <p>
            Game Rank permite a los usuarios publicar reseñas, puntuaciones y otros contenidos (colectivamente,
            "Contenido del Usuario"). Al publicar dicho contenido, declaras y garantizas que:
          </p>
          <ul class="terminos-list">
            <li>Eres el propietario o tienes los derechos necesarios para publicar dicho contenido.</li>
            <li>El contenido no infringe derechos de propiedad intelectual, privacidad o cualquier otro derecho de terceros.</li>
            <li>El contenido es auténtico, refleja tu opinión personal y no ha sido fabricado o incentivado artificialmente.</li>
          </ul>
          <p>
            Al publicar contenido en Game Rank, nos otorgas una licencia no exclusiva, gratuita, mundial
            y sublicenciable para usar, reproducir, modificar, distribuir y mostrar dicho contenido en el
            contexto de la Plataforma. Nos reservamos el derecho de eliminar cualquier contenido que
            consideremos inapropiado o que infrinja estos términos, sin necesidad de justificación previa.
          </p>
        </section>

        <section id="propiedad" class="terminos-section">
          <div class="section-num">06</div>
          <h2>Propiedad Intelectual y Atribución de Contenido</h2>
          <p>
            Todo el contenido relativo a videojuegos mostrado en Game Rank —incluyendo títulos, descripciones,
            imágenes de portada, fechas de lanzamiento, géneros, plataformas y demás metadatos— es
            proporcionado íntegramente por <strong>RAWG Video Games Database</strong>
            (<a href="https://rawg.io" target="_blank" rel="noopener noreferrer" class="terminos-inline-link">rawg.io</a>),
            un servicio externo de terceros.
          </p>
          <p>
            Game Rank actúa exclusivamente como plataforma de visualización y organización de dicha información.
            No generamos, verificamos ni somos responsables de la exactitud, integridad o actualización del
            contenido de videojuegos. Todos los derechos sobre esos datos pertenecen a RAWG y a los
            respectivos titulares de cada propiedad intelectual (desarrolladoras y distribuidoras de videojuegos).
          </p>
          <p>
            Los elementos propios de Game Rank —diseño de la interfaz, código fuente, logotipo y textos
            editoriales elaborados por el equipo— están protegidos por las leyes de propiedad intelectual
            aplicables y no pueden ser reproducidos ni distribuidos sin autorización expresa.
          </p>
          <div class="terminos-attribution-note">
            <i class="pi pi-database"></i>
            <div>
              <strong>Datos de videojuegos proporcionados por RAWG</strong>
              <span>Game Rank utiliza la API de RAWG para obtener información sobre videojuegos. RAWG es el propietario
              de dicha base de datos y su uso está sujeto a los términos de servicio de RAWG.</span>
            </div>
          </div>
        </section>

        <section id="privacidad" class="terminos-section">
          <div class="section-num">07</div>
          <h2>Privacidad y Datos Personales</h2>
          <p>
            Game Rank recopila y trata datos personales necesarios para la prestación del servicio, como
            nombre, apellidos y dirección de correo electrónico proporcionados durante el registro.
          </p>
          <p>
            Nos comprometemos a:
          </p>
          <ul class="terminos-list">
            <li>No vender, alquilar ni ceder tus datos personales a terceros con fines comerciales.</li>
            <li>Aplicar medidas de seguridad técnicas y organizativas adecuadas para proteger tu información.</li>
            <li>Almacenar únicamente los datos necesarios para la prestación del servicio.</li>
            <li>Respetar tu derecho de acceso, rectificación y supresión de tus datos mediante la eliminación de cuenta disponible en tu perfil.</li>
          </ul>
          <p>
            Las contraseñas se almacenan cifradas y nunca son accesibles en texto plano. Game Rank no almacena
            información de pago, ya que la Plataforma es completamente gratuita.
          </p>
        </section>

        <section id="responsabilidad" class="terminos-section">
          <div class="section-num">08</div>
          <h2>Limitación de Responsabilidad</h2>
          <p>
            Game Rank se proporciona "tal cual" y "según disponibilidad". No garantizamos que la Plataforma
            esté libre de errores, interrupciones o que los datos mostrados sean siempre precisos o actualizados.
          </p>
          <p>
            En la máxima medida permitida por la ley aplicable, Game Rank no será responsable de:
          </p>
          <ul class="terminos-list">
            <li>Pérdidas indirectas, incidentales o consecuentes derivadas del uso o imposibilidad de uso de la Plataforma.</li>
            <li>Inexactitudes en la información de videojuegos obtenida a través de servicios de terceros.</li>
            <li>Contenido publicado por otros usuarios de la Plataforma.</li>
            <li>Interrupciones temporales del servicio por mantenimiento, actualizaciones o causas de fuerza mayor.</li>
          </ul>
        </section>

        <section id="modificaciones" class="terminos-section">
          <div class="section-num">09</div>
          <h2>Modificaciones del Servicio y los Términos</h2>
          <p>
            Game Rank se reserva el derecho de modificar estos Términos y Condiciones en cualquier momento.
            Los cambios entrarán en vigor desde el momento de su publicación en la Plataforma. Te notificaremos
            de cambios significativos mediante un aviso visible en la Plataforma o a través del correo
            electrónico asociado a tu cuenta.
          </p>
          <p>
            El uso continuado de Game Rank tras la publicación de cambios implica la aceptación de los
            nuevos términos. Si no estás de acuerdo con los cambios, debes dejar de usar la Plataforma
            y puedes solicitar la eliminación de tu cuenta desde tu perfil.
          </p>
        </section>

        <section id="terminacion" class="terminos-section">
          <div class="section-num">10</div>
          <h2>Terminación de la Cuenta</h2>
          <p>
            Puedes eliminar tu cuenta en cualquier momento desde la sección de perfil de usuario. La eliminación
            de la cuenta conllevará la supresión permanente de todos tus datos asociados, incluyendo
            reseñas, puntuaciones, colecciones y favoritos. Esta acción es irreversible.
          </p>
          <p>
            Game Rank podrá suspender o cancelar tu cuenta sin previo aviso si determina que has infringido
            estos Términos y Condiciones o si tu comportamiento resulta perjudicial para la comunidad
            o para el correcto funcionamiento de la Plataforma.
          </p>
        </section>

        <section id="contacto" class="terminos-section">
          <div class="section-num">11</div>
          <h2>Contacto</h2>
          <p>
            Si tienes preguntas, dudas o sugerencias relacionadas con estos Términos y Condiciones,
            puedes ponerte en contacto con nosotros a través del repositorio del proyecto en GitHub:
          </p>
          <a href="https://github.com/Alan3420" target="_blank" rel="noopener noreferrer" class="terminos-contact-link">
            <i class="pi pi-github"></i>
            github.com/Alan3420
          </a>
        </section>

        <div class="terminos-footer-note">
          <i class="pi pi-info-circle"></i>
          Estos términos fueron redactados el 15 de mayo de 2026 y son aplicables a todos los usuarios de Game Rank
          a partir de dicha fecha.
        </div>

      </article>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TerminosCondiciones',
  data() {
    return {
      seccionActiva: '',
      secciones: [
        { id: 'aceptacion',     num: '01', titulo: 'Aceptación' },
        { id: 'descripcion',    num: '02', titulo: 'Descripción del Servicio' },
        { id: 'cuenta',         num: '03', titulo: 'Registro y Cuenta' },
        { id: 'uso-aceptable',  num: '04', titulo: 'Uso Aceptable' },
        { id: 'contenido',      num: '05', titulo: 'Contenido del Usuario' },
        { id: 'propiedad',      num: '06', titulo: 'Propiedad Intelectual' },
        { id: 'privacidad',     num: '07', titulo: 'Privacidad y Datos' },
        { id: 'responsabilidad',num: '08', titulo: 'Limitación de Responsabilidad' },
        { id: 'modificaciones', num: '09', titulo: 'Modificaciones' },
        { id: 'terminacion',    num: '10', titulo: 'Terminación de Cuenta' },
        { id: 'contacto',       num: '11', titulo: 'Contacto' },
      ]
    };
  },
  mounted() {
    this.observer = new IntersectionObserver(this.onIntersect, {
      rootMargin: '-30% 0px -60% 0px'
    });
    this.$nextTick(() => {
      this.secciones.forEach(s => {
        const el = document.getElementById(s.id);
        if (el) this.observer.observe(el);
      });
    });
  },
  beforeUnmount() {
    if (this.observer) this.observer.disconnect();
  },
  methods: {
    scrollTo(id) {
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },
    onIntersect(entries) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.seccionActiva = entry.target.id;
        }
      });
    }
  }
};
</script>

<style scoped src="./style_terminos.css"></style>
