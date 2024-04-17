<template>
<div>
  <nav class="bg-dark">
    <router-link to='/home'
                 style="font-size: 45px"
                 class="text-style"
                 :class="{disabled: $route.meta.hideNavbar}">Bloglite</router-link>
  </nav>
  <nav class="navbar navbar-expand-lg navbar-light bg-dark">
  <div v-if="!$route.meta.hideNavbar" class="collapse navbar-collapse" id="navbarNav"  style="margin-bottom: -10px">
    <ul class="navbar-nav">
      &nbsp;&nbsp;&nbsp;
      <li class="nav-item active">
        <router-link to="/home" class="text-style btn home" tag="button"></router-link>
      </li> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <li class="nav-item active">
        <router-link to="/profile" class="text-style btn profile" tag="button"></router-link>
      </li>
    </ul>
  </div>
</nav>
  </div>
</template>

<script>
export default {
  methods:{
  }
}
</script>

<style scoped>
.text-style{
  text-align: left !important;
  font-size:30px;
  text-decoration: none !important;
  font-family: fantasy !important;
  color: floralwhite !important;
}
.disabled {
  pointer-events: none;
}
.home{
  width: 75px;
  height: 70px;
  background-image: url(https://cdn-icons-png.flaticon.com/512/1946/1946488.png);
  background-color:white;
  background-size: 100%;
  background-repeat: no-repeat;
  background-clip: padding-box;
}
.profile{
  width: 75px;
  height: 72px;
  background-image: url(https://cdn-icons-png.flaticon.com/512/1144/1144760.png);
  background-color:white;
  background-size: 100%;
  background-repeat: no-repeat;
  background-clip: border-box;
}
</style>