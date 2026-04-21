# Image Nginx légère pour servir le frontend statique
FROM nginx:alpine

# Copie le fichier HTML dans le dossier servi par Nginx
COPY index.html /usr/share/nginx/html/index.html

# Expose le port 80 (standard HTTP)
EXPOSE 80

# Nginx démarre automatiquement
CMD ["nginx", "-g", "daemon off;"]
