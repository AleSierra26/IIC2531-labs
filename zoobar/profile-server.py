#!/usr/bin/env python3

import base64
import rpclib
import sys
import os
import sandboxlib
import hashlib
import socket
import bank
import bank_client
import zoodb

sys.path.append(os.getcwd())
import readconf

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor, pcode, ct):
        self.user = user
        self.visitor = visitor
        self.pcode = pcode
        self.ct = ct

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        return bank_client.get_log(username)

    def rpc_get_user_info(self, username):
        return {
            'username': self.user,
            'profile': self.pcode,
            'zoobars': bank.zoobars(username),
        }

    def rpc_xfer(self, target, zoobars):
        bank.transfer(self.user, target, zoobars, token=None)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec(pcode, globals)

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, pcode, user, visitor):
        # UID para ejecutar sandbox (no-root)
        SBOX_UID = 6858
        SBOX_GID = 6858

        # Base donde crearemos subdirs para cada usuario sandboxed
        base_profiles_dir = '/tmp/profiles'

        # Crear nombre de directorio seguro a partir del username
        # (evita problemas con caracteres especiales -> usamos hash)
        safe_name = hashlib.sha256(user.encode('utf-8')).hexdigest()[:32]
        userdir = os.path.join(base_profiles_dir, safe_name)

        # Asegurar que el directorio base exista
        try:
            os.makedirs(base_profiles_dir, exist_ok=True)
        except Exception as e:
            log(f"profile_server: could not create base_profiles_dir {base_profiles_dir}: {e}")
            # continuar, porque probablemente ya existe o fallará al intentar crear userdir

        # Crear (si es necesario) el directorio del usuario y ajustar propietario/permisos
        try:
            if not os.path.exists(userdir):
                os.makedirs(userdir, exist_ok=True)
            # chown/chmod al uid/gid para que solo ese uid pueda acceder
            try:
                # Usamos numeric uid/gid; no dependemos de entradas en /etc/passwd
                os.chown(userdir, SBOX_UID, SBOX_GID)
            except PermissionError:
                log(f"profile_server: permission error chown {userdir} -> uid {SBOX_UID}")
            except OSError as e:
                log(f"profile_server: os.chown failed for {userdir}: {e}")

            # Permisos privados: solo propietario puede leer/ejecutar/escribir
            try:
                os.chmod(userdir, 0o700)
            except OSError as e:
                log(f"profile_server: chmod failed for {userdir}: {e}")
        except Exception as e:
            log(f"profile_server: could not prepare userdir {userdir}: {e}")
            # si no podemos preparar el userdir, mejor fallar la ejecución del perfil
            return "Error preparing profile storage"

        # Lockfile dentro del userdir (único por UID / por usuario)
        lockfile = os.path.join(userdir, 'lockfile')

        # preparar socketpair + fork del ProfileAPIServer (igual que antes)
        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            # hijo que a su vez crea el proceso del ProfileAPIServer
            if os.fork() <= 0:
                sa.close()
                ct = readconf.read_conf()
                ProfileAPIServer(user, visitor, pcode, ct).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        # Crear sandbox con userdir y UID no-root; pasar lockfile dentro del directorio
        sandbox = sandboxlib.Sandbox(userdir, SBOX_UID, lockfile)
        with rpclib.RpcClient(sa) as profile_api_client:
            # Ejecutar en sandbox la función que corre el perfil.
            # Sandbox.run() hará chroot(userdir), setresuid(SBOX_UID), setrlimit, unshare, etc.
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))


if len(sys.argv) != 2:
    print(sys.argv[0], "too few args")

s = ProfileServer()
s.run_fork(sys.argv[1])
