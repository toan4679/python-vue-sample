import { createApp, ref, onMounted } from "vue";

createApp({
  setup() {
    const hello = ref("đang tải...");
    const db = ref(null);
    onMounted(async () => {
      try { hello.value = (await (await fetch("/api/hello")).json()).message; } catch { hello.value = "lỗi gọi API"; }
      try { db.value = await (await fetch("/api/db")).json(); } catch { db.value = { error: true }; }
    });
    return { hello, db };
  },
  template: `<main style="font-family:sans-serif;padding:24px">
    <h1>Sample: Python + Vue</h1><p>Backend nói: {{ hello }}</p><pre>DB: {{ JSON.stringify(db) }}</pre></main>`,
}).mount("#app");
