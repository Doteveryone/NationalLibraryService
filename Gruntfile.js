module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      target: {
        files: [
          {
            expand: true,
            cwd: 'nls/assets/javascript',
            src: ['*.js'], 
            dest: 'nls/static/javascript', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'nls/assets/vendor/foundation-sites/dist',
            src: ['**/*.js'], 
            dest: 'nls/static/vendor/foundation-sites', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'nls/assets/vendor/jquery/dist',
            src: ['**/*.js'], 
            dest: 'nls/static/vendor/jquery', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'nls/assets/vendor/leaflet/dist',
            src: ['**/*.*'], 
            dest: 'nls/static/vendor/leaflet', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'nls/assets/vendor/chatjs/ChatJs',
            src: ['**/*.*'], 
            dest: 'nls/static/vendor/chatjs', 
            filter: 'isFile'
          }
        ]
      }
    },
    sass: {
      options: {
        loadPath: ['nls/assets/vendor/foundation-sites/scss']
      },
      dist: {
        files: {
          'nls/static/css/main.css' : 'nls/assets/sass/main.scss',
          'nls/static/css/register.css' : 'nls/assets/sass/register.scss'
        }
      }
    },
    watch: {
      css: {
        files: '**/*.scss',
        tasks: ['sass']
      },
      scripts: {
        files: 'nls/assets/**/*.js',
        tasks: ['copy']
      },
      scripts: {
        files: 'nls/assets/**/*.css',
        tasks: ['copy']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.registerTask('default',['watch']);
}