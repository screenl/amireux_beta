<script setup>
    import { onMounted, ref } from "vue";
    import { invoke } from "@tauri-apps/api/primitives";
    const report = ref("");
    const username = ref("");
    const analysis = ref("");
    onMounted(async () => {
        username.value = await invoke("get_username",{});
        analysis.value = await invoke("get_analysis",{});
    });
</script>

<template>
     
    <div class="imessage">
     <div class="card">
        <div class = "report-card-head">
            <img class="card_avatar" src="../assets/dog.jpg" alt="Avatar">
            <p><b>{{username}}</b></p>
        </div>
        <div class="container">
            <h3>Personality Report:</h3>
            <p>{{ analysis }}</p>
        </div>

        <div class="dog-ear"></div>
        </div> 
    </div>
</template>