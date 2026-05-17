<template>
  <div class="terminos-page">

    <!-- Hero -->
    <div class="terminos-hero">
      <div class="terminos-hero-inner">
        <span class="terminos-eyebrow">
          <i class="pi pi-shield"></i>
          Legal
        </span>
        <h1>Terms and Conditions</h1>
        <p>Last updated: May 15, 2026</p>
      </div>
    </div>

    <div class="terminos-layout">

      <!-- TOC lateral -->
      <aside class="terminos-toc">
        <p class="toc-title">Contents</p>
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
          <h2>Acceptance of Terms</h2>
          <p>
            By accessing or using Game Rank (hereinafter, "the Platform"), you agree to be bound by these
            Terms and Conditions, as well as our Privacy Policy. If you disagree with any
            of these provisions, please do not use the Platform.
          </p>
          <p>
            These terms apply to all visitors, registered users and any person who accesses
            or uses the services offered by Game Rank.
          </p>
        </section>

        <section id="descripcion" class="terminos-section">
          <div class="section-num">02</div>
          <h2>Description of Service</h2>
          <p>
            Game Rank is a platform dedicated to cataloguing, rating and discovering video games.
            The services we offer include, among others:
          </p>
          <ul class="terminos-list">
            <li>Exploration of an extensive video game catalogue with detailed information.</li>
            <li>Community-driven scoring and review system.</li>
            <li>Management of personal collections and favorites lists.</li>
            <li>Game status tracking (playing, completed, pending, abandoned, wishlist).</li>
            <li>Information on upcoming industry releases.</li>
          </ul>
          <p>
            Video game information is obtained through the RAWG API (rawg.io), an
            external service over which Game Rank has no editorial control. We reserve the right to expand,
            modify or discontinue any of these services at any time.
          </p>
        </section>

        <section id="cuenta" class="terminos-section">
          <div class="section-num">03</div>
          <h2>Registration and User Account</h2>
          <p>
            To access the full features of Game Rank, creating an account is required. By doing so,
            you agree to:
          </p>
          <ul class="terminos-list">
            <li>Provide truthful, complete and up-to-date information during registration.</li>
            <li>Maintain the confidentiality of your access credentials (email address and password).</li>
            <li>Notify us immediately of any unauthorized use of your account.</li>
            <li>Be solely responsible for all activities carried out under your account.</li>
            <li>Not transfer, assign or share access to your account with third parties.</li>
          </ul>
          <p>
            Game Rank reserves the right to suspend or delete accounts that violate these terms,
            without prior notice and without any obligation to refund.
          </p>
        </section>

        <section id="uso-aceptable" class="terminos-section">
          <div class="section-num">04</div>
          <h2>Acceptable Use</h2>
          <p>
            By using Game Rank, you agree not to engage in any of the following conduct:
          </p>
          <ul class="terminos-list">
            <li>Post false, misleading, defamatory, obscene, offensive content or content that infringes third-party rights.</li>
            <li>Harass, threaten or intimidate other users of the Platform.</li>
            <li>Attempt to gain unauthorized access to systems, accounts or data of the Platform.</li>
            <li>Use bots, scrapers or other automated tools to extract content from Game Rank.</li>
            <li>Interfere with or disrupt the integrity or performance of the Platform.</li>
            <li>Post spam, unsolicited advertising or repetitive content in bulk.</li>
            <li>Impersonate another person or entity.</li>
            <li>Carry out any activity that violates applicable law.</li>
          </ul>
        </section>

        <section id="contenido" class="terminos-section">
          <div class="section-num">05</div>
          <h2>User Content</h2>
          <p>
            Game Rank allows users to post reviews, ratings and other content (collectively,
            "User Content"). By posting such content, you represent and warrant that:
          </p>
          <ul class="terminos-list">
            <li>You own or have the necessary rights to post such content.</li>
            <li>The content does not infringe intellectual property rights, privacy or any other third-party rights.</li>
            <li>The content is authentic, reflects your personal opinion and has not been fabricated or artificially incentivized.</li>
          </ul>
          <p>
            By posting content on Game Rank, you grant us a non-exclusive, royalty-free, worldwide
            and sublicensable license to use, reproduce, modify, distribute and display such content in the
            context of the Platform. We reserve the right to remove any content we
            deem inappropriate or that violates these terms, without prior justification.
          </p>
        </section>

        <section id="propiedad" class="terminos-section">
          <div class="section-num">06</div>
          <h2>Intellectual Property and Content Attribution</h2>
          <p>
            All video game content displayed on Game Rank — including titles, descriptions,
            cover images, release dates, genres, platforms and other metadata — is
            provided entirely by <strong>RAWG Video Games Database</strong>
            (<a href="https://rawg.io" target="_blank" rel="noopener noreferrer" class="terminos-inline-link">rawg.io</a>),
            a third-party external service.
          </p>
          <p>
            Game Rank acts solely as a platform for displaying and organizing this information.
            We do not generate, verify or take responsibility for the accuracy, completeness or currency of
            video game content. All rights to such data belong to RAWG and the
            respective intellectual property holders (video game developers and publishers).
          </p>
          <p>
            Elements owned by Game Rank — interface design, source code, logo and editorial texts
            produced by the team — are protected by applicable intellectual property laws
            and may not be reproduced or distributed without express authorization.
          </p>
          <div class="terminos-attribution-note">
            <i class="pi pi-database"></i>
            <div>
              <strong>Video game data provided by RAWG</strong>
              <span>Game Rank uses the RAWG API to obtain information about video games. RAWG is the owner
              of said database and its use is subject to RAWG's terms of service.</span>
            </div>
          </div>
        </section>

        <section id="privacidad" class="terminos-section">
          <div class="section-num">07</div>
          <h2>Privacy and Personal Data</h2>
          <p>
            Game Rank collects and processes personal data necessary to provide the service, such as
            first name, last name and email address provided during registration.
          </p>
          <p>
            We commit to:
          </p>
          <ul class="terminos-list">
            <li>Not selling, renting or transferring your personal data to third parties for commercial purposes.</li>
            <li>Applying adequate technical and organizational security measures to protect your information.</li>
            <li>Storing only the data necessary to provide the service.</li>
            <li>Respecting your right of access, rectification and deletion of your data through the account deletion available in your profile.</li>
          </ul>
          <p>
            Passwords are stored encrypted and are never accessible in plain text. Game Rank does not store
            payment information, as the Platform is completely free.
          </p>
        </section>

        <section id="responsabilidad" class="terminos-section">
          <div class="section-num">08</div>
          <h2>Limitation of Liability</h2>
          <p>
            Game Rank is provided "as is" and "as available". We do not guarantee that the Platform
            will be error-free, uninterrupted, or that the data displayed will always be accurate or up to date.
          </p>
          <p>
            To the fullest extent permitted by applicable law, Game Rank shall not be liable for:
          </p>
          <ul class="terminos-list">
            <li>Indirect, incidental or consequential losses arising from the use or inability to use the Platform.</li>
            <li>Inaccuracies in video game information obtained through third-party services.</li>
            <li>Content posted by other users of the Platform.</li>
            <li>Temporary service interruptions due to maintenance, updates or force majeure events.</li>
          </ul>
        </section>

        <section id="modificaciones" class="terminos-section">
          <div class="section-num">09</div>
          <h2>Modifications to the Service and Terms</h2>
          <p>
            Game Rank reserves the right to modify these Terms and Conditions at any time.
            Changes will take effect from the moment they are published on the Platform. We will notify you
            of significant changes through a visible notice on the Platform or via the email address
            associated with your account.
          </p>
          <p>
            Continued use of Game Rank after the publication of changes implies acceptance of the
            new terms. If you disagree with the changes, you must stop using the Platform
            and may request deletion of your account from your profile.
          </p>
        </section>

        <section id="terminacion" class="terminos-section">
          <div class="section-num">10</div>
          <h2>Account Termination</h2>
          <p>
            You may delete your account at any time from the user profile section. Deleting
            your account will result in the permanent deletion of all associated data, including
            reviews, ratings, collections and favorites. This action is irreversible.
          </p>
          <p>
            Game Rank may suspend or cancel your account without prior notice if it determines that you have violated
            these Terms and Conditions or if your behavior is harmful to the community
            or to the proper functioning of the Platform.
          </p>
        </section>

        <section id="contacto" class="terminos-section">
          <div class="section-num">11</div>
          <h2>Contact</h2>
          <p>
            If you have questions, doubts or suggestions related to these Terms and Conditions,
            you can contact us through the project repository on GitHub:
          </p>
          <a href="https://github.com/Alan3420" target="_blank" rel="noopener noreferrer" class="terminos-contact-link">
            <i class="pi pi-github"></i>
            github.com/Alan3420
          </a>
        </section>

        <div class="terminos-footer-note">
          <i class="pi pi-info-circle"></i>
          These terms were drafted on May 15, 2026 and apply to all Game Rank users
          from that date.
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
        { id: 'aceptacion',     num: '01', titulo: 'Acceptance' },
        { id: 'descripcion',    num: '02', titulo: 'Description of Service' },
        { id: 'cuenta',         num: '03', titulo: 'Registration & Account' },
        { id: 'uso-aceptable',  num: '04', titulo: 'Acceptable Use' },
        { id: 'contenido',      num: '05', titulo: 'User Content' },
        { id: 'propiedad',      num: '06', titulo: 'Intellectual Property' },
        { id: 'privacidad',     num: '07', titulo: 'Privacy & Data' },
        { id: 'responsabilidad',num: '08', titulo: 'Limitation of Liability' },
        { id: 'modificaciones', num: '09', titulo: 'Modifications' },
        { id: 'terminacion',    num: '10', titulo: 'Account Termination' },
        { id: 'contacto',       num: '11', titulo: 'Contact' },
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
