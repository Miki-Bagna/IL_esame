<template>
  <div class="container">
    <h1>Carica lo script di un film!</h1>
    <hr class="mt-3" />
    <div class="d-flex">
      <div class="input-group">
        <input type="file" class="form-control" id="inputGroupFile02" accept=".txt" @change="handleFileUpload" />
      </div>
      <button class="btn btn-primary ms-2" @click="submitFile(); ">Analizza</button>
    </div>
    <div class="mt-5">
      <div v-if="loading_summary" class="d-flex">
        <div class="spinner-border me-3" role="status"></div>
        <p>Elaborazione del riassunto...</p>
      </div>
      <div v-if="!loading_summary && loading_characters" class="d-flex">
        <div class="spinner-border me-3" role="status"></div>
        <p>Estrazione dei personaggi...</p>
      </div>
      <div v-if="!loading_characters && !loading_summary && data && summary">
        <h5>Riassunto dello script</h5>
        <p class="bg-light p-3 rounded mb-5">{{ summary }}</p>
        <h5>Personaggi principali rilevati nello script</h5>
        <button :class="['btn', 'rounded-pill', 'me-2', 'mt-2', selectedCharacter && selectedCharacter.name === name ? 'btn-primary' : 'btn-outline-primary']" v-for="(value, name) in data" :key="name" @click="chart(name, value)">{{ name }}</button>
        <div v-if="selectedCharacter" class="mt-5">
          <h5>Bubble chart di {{ selectedCharacter.name }}</h5>
          <div class="d-flex justify-content-center bg-light p-2 rounded">
            <D3 :key="selectedCharacter.name" :name="selectedCharacter.name" :data="selectedCharacter.data" /> 
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import D3 from '../components/D3.vue'

export default {
  components: {
    D3
  },
  data() {
    return {
      uploadedFile: null,
      loading_characters: false,
      loading_summary: false,
      data: null,
      sentences: null,
      selectedCharacter: null,
      summary: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.uploadedFile = event.target.files[0];
    },
    submitFile() {
      if (this.uploadedFile && this.uploadedFile.type === "text/plain") {
        this.loading_summary = true;
        this.loading_characters = true;
        const formData = new FormData();
        formData.append('file', this.uploadedFile);

        axios.post('http://localhost:5001/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          if (response.data) {
            this.loading_characters = false;
            this.data = response.data.characters_sentences;
            this.sentences = response.data.all_sentences;
            console.log(this.sentences);
          }
        })
        .catch(error => {
          this.loading_characters = false;
          console.error("Errore nell'invio del file:", error);
        });

        axios.post('http://localhost:5001/up_summ', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          if (response.data) {
            this.loading_summary = false;
            this.summary = response.data.script_summary;
            console.log(this.summary);
          }
        })
        .catch(error => {
          this.loading_summary = false;
          console.error("Errore nell'invio del file:", error);
        });

      } else {
        alert("il file non è supportato");
      }
    },
    chart(name, value) {
      this.selectedCharacter = { name, data: value };
    }
  },
};
</script>
