<template>
<div class="container mt-4">
  <form @submit.prevent="insertPost">
    <input
    type="text"
    class="form-control"
    placeholder="Please enter your title"
    v-model="title"/>
    <br/>
    <textarea
        rows="10"
        class="form-control"
        placeholder="Please enter the body of your post"
        v-model="body">
    </textarea>
    <br/>
    <input
        type="file"
        accept="image/*"
        class="form-control"
        @change="uploadImage"
    />
    <div id="preview">
    <img v-if="image.imageUrl"
         :src="image.imageUrl"
         :alt="'Preview Image'"/>
  </div>

    <button
    class="btn btn-success mt-4">
      Publish Blog
    </button>
  </form>
  <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
    <strong>{{error}}</strong>
  </div>
  <br><br>
  <div>
    <h4>
      OR
      <br><br>
      <input
        type="file"
        accept=".csv"
        @change="uploadCSV"
        style="font-size: large; width: 300px"
    />
      <button class="btn btn-success" @click="importPost">Import Blog as CSV</button>
    </h4><span style="margin-right: 230px; font-size: small">(format as title, body, image url)</span><br>
    <div style="margin-right: 200px">
      <span style="font-size: xx-small;">
      If you are using WSL, be mindful while providing URLs.
    </span>
    <br>
    <span style="font-size: xx-small;">
      If your image url is of the form "C://path" or "D://path", convert it to
      /mnt/c/path or /mnt/d/path.
    </span>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data(){
    return{
      title:null,
      body:null,
      error:null,
      image:{
        image:null,
        imageUrl:null
      },
      csv:null
    }
  },
  methods:{
    insertPost(){
      if(!this.title||!this.body||!this.image.image)
        {
          this.error = "Please add all fields"
        }
      else
        {
          if (!(this.$store.state.token))
          {
            this.$store.state.user = JSON.parse(localStorage['user'])
            this.$store.state.token = localStorage['token']
          }
          let formData = new FormData();
          formData.append('title', this.title);
          formData.append('body', this.body);
          formData.append('image', this.image.image, this.image.image.name);
          fetch('http://localhost:5000/api/userposts',{
          method:"POST",
          headers:{
            "Authentication-Token":this.$store.state.token
          },
            body:formData
        })
            .then(resp => resp.json())
                .then(()=>{
                  this.$router.push({
                    name:"profile"
                  })
                })
                .catch(error => console.log(error))
        }
      },

    async importPost(){
      if (!(this.$store.state.token))
          {
            this.$store.state.user = JSON.parse(localStorage['user'])
            this.$store.state.token = localStorage['token']
          }
      if (!(this.csv)){
        this.error = "Please select CSV file"
      }
      else {
        let formData = new FormData();
        formData.append('csv', this.csv, this.csv.name);
        let response =  await fetch('http://localhost:5000/api/job', {
          method: "POST",
          headers: {
            "Authentication-Token": this.$store.state.token
          },
          body: formData
        })
        console.log(response)
            if (response.status !== 200){
              this.error = "Your image link seems to be wrong"
            }
            else{
              await this.$router.push({
                name: "profile"
              })
            }
      }
    },

    uploadImage(e){
      const file = e.target.files[0]
      this.image.image = file
      this.image.imageUrl = URL.createObjectURL(file)
      console.log(file)
    },

    uploadCSV(e){
      const file = e.target.files[0]
      this.csv = file
      console.log(file)
    }
    }
  }
</script>

<style scoped>

</style>