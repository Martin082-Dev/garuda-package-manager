pkgname=garuda-package-manager
pkgver=1.1
pkgrel=47
pkgdesc="Gestore avanzato di pacchetti, aggiornamenti e manutenzione per Garuda Linux"
arch=('any')
url="https://github.com/tuo-username/garuda-package-manager"
license=('MIT')
depends=('python' 'python-pyqt6' 'paru' 'flatpak')
optdepends=('pacman-contrib: per checkupdates e paccache (pulizia cache e controllo aggiornamenti più veloce)')
source=('garuda-package-manager.py' 'garuda-package-manager.desktop' 'garuda-package-manager.sh')
sha256sums=('SKIP' 'SKIP' 'SKIP')

package() {
    # Installa lo script principale in /opt con il nuovo nome
    install -Dm755 "$srcdir/garuda-package-manager.py" "$pkgdir/opt/garuda-package-manager/garuda-package-manager.py"

    # Installa il comando globale in /usr/bin
    install -Dm755 "$srcdir/garuda-package-manager.sh" "$pkgdir/usr/bin/garuda-package-manager"

    # Installa il lanciatore grafico nel menu applicazioni di sistema
    install -Dm644 "$srcdir/garuda-package-manager.desktop" "$pkgdir/usr/share/applications/garuda-package-manager.desktop"
}
