<template>
  <div class="container mt-5">
    <h2 class="mb-4">📢 Créer une Newsletter</h2>

    <div class="mb-3">
      <label for="subject" class="form-label">Objet</label>
      <input v-model="subject" type="text" class="form-control" id="subject" placeholder="Titre de la newsletter" />
    </div>

    <div class="mb-3">
      <label class="form-label">Contenu</label>

      <div v-if="editor">
        <div class="editor-toolbar mb-2">
          <button
            v-for="(item, index) in getToolbarItems()"
            :key="index"
            type="button"
            class="btn btn-sm me-2"
            :class="item.active() ? 'btn-primary' : 'btn-outline-secondary'"
            @click="item.command"
          >
            {{ item.label }}
          </button>
        </div>

        <EditorContent :editor="editor" class="editor-content border p-3 rounded bg-white" />
      </div>
      <div v-else class="text-muted">Chargement de l’éditeur...</div>
    </div>

    <div class="text-end">
      <button class="btn btn-success" @click="sendNewsletter" :disabled="loading">
        📨 Envoyer
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Color from '@tiptap/extension-color'
import Link from '@tiptap/extension-link'
import Heading from '@tiptap/extension-heading'
import axios from 'axios'

const subject = ref('')
const loading = ref(false)

const editor = useEditor({
  content: '',
  extensions: [
    StarterKit,
    Underline,
    Color,
    Link.configure({ openOnClick: false }),
    Heading.configure({ levels: [1, 2] }),
    TextAlign.configure({ types: ['heading', 'paragraph'] }),
  ],
  editorProps: {
    attributes: {
      class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl focus:outline-none',
    },
  },
})

const getToolbarItems = () => {
  if (!editor.value) return []

  return [
    { label: 'Gras', command: () => editor.value.chain().focus().toggleBold().run(), active: () => editor.value.isActive('bold') },
    { label: 'Italique', command: () => editor.value.chain().focus().toggleItalic().run(), active: () => editor.value.isActive('italic') },
    { label: 'Souligné', command: () => editor.value.chain().focus().toggleUnderline().run(), active: () => editor.value.isActive('underline') },
    { label: 'Liste •', command: () => editor.value.chain().focus().toggleBulletList().run(), active: () => editor.value.isActive('bulletList') },
    { label: 'Liste 1.', command: () => editor.value.chain().focus().toggleOrderedList().run(), active: () => editor.value.isActive('orderedList') },
    { label: 'Code', command: () => editor.value.chain().focus().toggleCode().run(), active: () => editor.value.isActive('code') },
    { label: 'Citation', command: () => editor.value.chain().focus().toggleBlockquote().run(), active: () => editor.value.isActive('blockquote') },
    {
      label: 'Lien',
      command: () => {
        const url = prompt('Entrez l’URL :')
        if (url) editor.value.chain().focus().setLink({ href: url }).run()
      },
      active: () => editor.value.isActive('link')
    },
    { label: 'Titre 1', command: () => editor.value.chain().focus().toggleHeading({ level: 1 }).run(), active: () => editor.value.isActive('heading', { level: 1 }) },
    { label: 'Titre 2', command: () => editor.value.chain().focus().toggleHeading({ level: 2 }).run(), active: () => editor.value.isActive('heading', { level: 2 }) },
  ]
}

const sendNewsletter = async () => {
  if (!subject.value || !editor.value?.getHTML()) {
    alert('Veuillez remplir tous les champs.')
    return
  }

  loading.value = true

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/newsletter/send/', {
      subject: subject.value,
      content: editor.value.getHTML(),
    })

    alert('✅ Newsletter envoyée avec succès.')
    subject.value = ''
    editor.value.commands.setContent('')
  } catch (err) {
    console.error('❌ Erreur envoi newsletter :', err)
    alert("Erreur lors de l'envoi.")
  } finally {
    loading.value = false
  }
}

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})
</script>

<style scoped>
.editor-toolbar {
  display: flex;
  flex-wrap: wrap;
}
.editor-content {
  min-height: 200px;
}
</style>
