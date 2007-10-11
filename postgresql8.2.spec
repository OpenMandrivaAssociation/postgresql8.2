%if %_lib == lib64
%define _requires_exceptions devel(libtcl8.4(64bit))
%else
%define _requires_exceptions devel(libtcl8.4)
%endif

%define pyver %(python -c 'import sys;print(sys.version[0:3])')
%define perl_version %(rpm -q --qf "%{VERSION}" perl)
%define perl_epoch %(rpm -q --qf "%{EPOCH}" perl)

%define pgdata /var/lib/pgsql
%define logrotatedir %{_sysconfdir}/logrotate.d

%define major 5
%define major_ecpg 5

%define bname postgresql
%define current_major_version 8.2
%define current_minor_version 5

%define release %mkrel 2

# For which mdv release this major is our default
%define produce_devel 0
%if %mdvver == 200800
%define produce_devel 1
%endif
# If major has not change during another release...
#%if %mdvver = 200810
#%define produce_devel 1
#%endif

# up to which mdv release this is hightest release
%define produce_client 0
%if %mdvver <= 200800
%define produce_client 1
%endif 

%define libname %mklibname pq %{major}
%define libnamedevel %mklibname -d pq
%define libecpg %mklibname ecpg %{major_ecpg}
%define libecpgdevel %mklibname -d ecpg

# Release of our script: soft/postgres-mdkupd in cvs
%define mdk_pg_ver 1.9

Summary: 	PostgreSQL client programs and libraries
Name:		%{bname}%{current_major_version}
Version: 	%{current_major_version}.%{current_minor_version}
Release: 	%release
License:	BSD
Group:		Databases
URL:		http://www.postgresql.org/ 
Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source5:	ftp://ftp.postgresql.orga/pub/source/v%{version}/postgresql-%{version}.tar.bz2.md5
Source11:	postgresql.init
# http://cvs.mandriva.com/cgi-bin/viewcvs.cgi/soft/postgres-mdkupd/
Source12:	postgresql-mdk-%{mdk_pg_ver}.tar.bz2
Source13:	postgresql.mdv.releasenote
Patch9:		postgresql-7.4.1-pkglibdir.diff
Patch11:	postgresql-7.4.5-CAN-2005-0227.patch
Requires:	perl
Provides:	postgresql-clients
Obsoletes:	postgresql-clients
BuildRequires:	XFree86-devel bison flex gettext termcap-devel ncurses-devel openssl-devel
BuildRequires:	pam-devel perl-devel python-devel readline-devel >= 4.3 tk zlib-devel tcl
BuildRequires:	tcl tcl-devel
# should libedit0 be moved to main?
BuildConflicts:	edit-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides: %{bname}-virtual = %{version}-%{release}
Conflicts: %{bname}-virtual < %{version}
Conflicts: %{bname}-virtual > %{version}
Obsoletes: %{bname} < %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the client
libraries for C and C++, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package -n %{bname}
Summary: 	PostgreSQL client programs and libraries
Group:		Databases
Requires:   %{name} = %{version}-%{release}

%description -n %{bname}
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the client
libraries for C and C++, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package -n	%{libname}
Summary:	The shared libraries required for any PostgreSQL clients
Group:		System/Libraries
Obsoletes:	postgresql-libs
Provides:	postgresql-libs = %{version}-%{release}
Provides:   libpq = %{version}-%{release}
# Avoid conflicts with lib having bad major
Conflicts:  libpq3 = 8.0.2

%description -n	%{libname}
C and C++ libraries to enable user programs to communicate with the
PostgreSQL database backend. The backend can be on another machine and
accessed through TCP/IP.

%package -n	%{libnamedevel}
Summary:	Development library for libpq
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	postgresql-libs-devel = %{version}-%{release}
Provides:   libpq-devel = %{version}-%{release}
Provides:       pq-devel = %{version}-%{release}
# Avoid conflicts with lib having bad major
Conflicts:  libpq3-devel = 8.0.2
Obsoletes:  %mklibname -d pq 5

%description -n	%{libnamedevel}
Development libraries for libpq

%package -n	%{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
Requires:	postgresql%{current_major_version} = %{version}-%{release}
Provides:	libecpg = %{version}-%{release}

%description -n	%{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C)
Use postgresql-dev to develop such programs.

%package -n	%{libecpgdevel}
Summary:	Development library to libecpg
Group:		Development/C
Requires:	%{libecpg} = %{version}-%{release}
Provides:	libecpg-devel = %{version}-%{release} 
Obsoletes:  %mklibname -d ecpg 5

%description -n	%{libecpgdevel}
Development library to libecpg.

%package	server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Databases
Provides:	sqlserver
Requires(post):   %{libname} >= %{version}-%{release}
Requires(preun):   %{libname} >= %{version}-%{release}
# add/remove services
Requires(post): rpm-helper
Requires(preun): rpm-helper
# add/del user
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	postgresql%{current_major_version} >= %{version}-%{release}
Requires(post):	postgresql%{current_major_version} >= %{version}-%{release}
Conflicts:	postgresql < 7.3
Provides: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-server-virtual = %{version}-%{release}
Conflicts: %{bname}-server-virtual < %{version}
Conflicts: %{bname}-server-virtual > %{version}

%description	server
The postgresql-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql and postgresql-devel packages.

After installing this package, please read postgresql.mdv.releasenote.

%package	docs
Summary:	Extra documentation for PostgreSQL
Group:		Databases
Provides: %{bname}-docs-virtual = %{version}-%{release}
Conflicts: %{bname}-docs-virtual < %{version}
Conflicts: %{bname}-docs-virtual > %{version}

%description	docs
The postgresql-docs package includes the SGML source for the documentation
as well as the documentation in other formats, and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package	contrib
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
Requires:   postgresql%{current_major_version}-server = %{version}-%{release}
Provides: %{bname}-contrib-virtual = %{version}-%{release}
Conflicts: %{bname}-contrib-virtual < %{version}
Conflicts: %{bname}-contrib-virtual > %{version}

%description	contrib
The postgresql-contrib package includes the contrib tree distributed with
the PostgreSQL tarball.  Selected contrib modules are prebuilt.

%package	devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Requires:	postgresql%{current_major_version} = %{version}-%{release}
Requires:   %{libnamedevel} = %{version}-%{release}
Requires:	%{libecpgdevel} = %{version}-%{release}
Provides: %{bname}-devel-virtual = %{version}-%{release}
Conflicts: %{bname}-devel-virtual < %{version}
Conflicts: %{bname}-devel-virtual > %{version}

%description	devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

%package	-n %{bname}-devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:  %bname-devel <= 8.2.4-1mdv

%description	-n %{bname}-devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

%package	pl
Summary:	Procedurals languages for PostgreSQL
Group:		Databases
Obsoletes:	libpgsql2
Requires:	%{name}-plpython = %{version}-%{release} 
Requires:	%{name}-plperl = %{version}-%{release} 
Requires:	%{name}-pltcl = %{version}-%{release} 
Requires:	%{name}-plpgsql = %{version}-%{release} 
Provides: %{bname}-pl-virtual = %{version}-%{release}
Conflicts: %{bname}-pl-virtual < %{version}
Conflicts: %{bname}-pl-virtual > %{version}

%description	pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl will install the the PL/Perl,
PL/Tcl, and PL/Python procedural languages for the backend.
PL/Pgsql is part of the core server package.

%package    plpython
Summary:    The PL/Python procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Conflicts:  postgresql-pl < %version-%release
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-plpython-virtual = %{version}-%{release}
Conflicts: %{bname}-plpython-virtual < %{version}
Conflicts: %{bname}-plpython-virtual > %{version}

%description	plpython
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plpython package contains the the PL/Python
procedural languages for the backend. PL/Python is part of the core 
server package.


%package    plperl
Summary:    The PL/Perl procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Requires:   perl-base = %{perl_epoch}:%{perl_version}
Conflicts:  postgresql-pl < %version-%release
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-plperl-virtual = %{version}-%{release}
Conflicts: %{bname}-plperl-virtual < %{version}
Conflicts: %{bname}-plperl-virtual > %{version}

%description	plperl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plperl package contains the the PL/Perl
procedural languages for the backend. PL/Perl is part of the core 
server package.

%package    pltcl
Summary:    The PL/Tcl procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Conflicts:  postgresql-pl < %version-%release
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-pltcl-virtual = %{version}-%{release}
Conflicts: %{bname}-pltcl-virtual < %{version}
Conflicts: %{bname}-pltcl-virtual > %{version}

%description	pltcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pltcl package contains the the PL/Tcl
procedural languages for the backend. PL/Tcl is part of the core 
server package.


%package    plpgsql
Summary:    The PL/PgSQL procedural language for PostgreSQL
Group:      Databases
Requires:   postgresql%{current_major_version}-server = %{version}
Conflicts:  postgresql-pl < %version-%release
Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides: %{bname}-plpgsql-virtual = %{version}-%{release}
Conflicts: %{bname}-plpgsql-virtual < %{version}
Conflicts: %{bname}-plpgsql-virtual > %{version}

%description	plpgsql
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plpgsql package contains the the PL/PgSQL
procedural languages for the backend. PL/PgSQL is part of the core 
server package.

%package	test
Summary:	The test suite distributed with PostgreSQL
Group:		Databases
Requires:	%{name} >= %{version}-%{release}
Requires:	%{name}-pl = %{version}-%{release}
Provides: %{bname}-test-virtual = %{version}-%{release}
Conflicts: %{bname}-test-virtual < %{version}
Conflicts: %{bname}-test-virtual > %{version}

%description	test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.

%prep

%setup -q -n %{bname}-%{version}

%patch9 -p0 -b .pkglibdir

%patch11 -p1 -b .can-2005-0227
#%patch13 -p1 -b .can-2005-0246

%setup -n %{bname}-%{version} -a12 -T -D -q

%build

pushd src
#(deush) if libtool exist, copy some files 
if [ -d %{_datadir}/libtool ]
then
   cp %{_datadir}/libtool/config.* .
fi

# doesn't build on PPC with full optimization (sb)
%ifnarch ppc
CFLAGS="${CFLAGS:-$RPM_OPT_FLAGS}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-$RPM_OPT_FLAGS}" ; export CXXFLAGS
%endif

#fix -ffast-math problem (deush)
%ifnarch ppc
%serverbuild
CFLAGS=`echo $RPM_OPT_FLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
%endif
popd

%configure --disable-rpath \
            --enable-hba \
	    --enable-locale \
	    --enable-multibyte \
	    --enable-syslog\
	    --with-CXX \
	    --enable-odbc \
	    --with-perl \
	    --with-python \
	    --with-tcl --with-tclconfig=%{_libdir} \
            --without-tk \
            --with-openssl \
            --with-pam \
            --libdir=%{_libdir} \
	    --datadir=%{_datadir}/pgsql \
	    --with-docdir=%{_docdir} \
	    --includedir=%{_includedir}/pgsql \
	    --mandir=%{_mandir} \
	    --prefix=%_prefix \
	    --sysconfdir=%{_sysconfdir}/pgsql \
            --enable-nls

# $(rpathdir) come from Makefile
perl -pi -e 's|^all:|LINK.shared=\$(COMPILER) -shared -Wl,-rpath,\$(rpathdir),-soname,\$(soname)\nall:|' src/pl/plperl/GNUmakefile


%make pkglibdir=%{_libdir}/pgsql all
%make -C contrib pkglibdir=%{_libdir}/pgsql all

pushd src/test
make all
popd

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT pkglibdir=%{_libdir}/pgsql install 
make -C contrib DESTDIR=$RPM_BUILD_ROOT pkglibdir=%{_libdir}/pgsql install

# install odbcinst.ini
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
install -m755 src/Makefile.global $RPM_BUILD_ROOT%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# Create the multiple postmaster startup directory
install -d -m 700 $RPM_BUILD_ROOT/etc/sysconfig/pgsql

# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pgsql/test
cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/
strip *.so
popd

mkdir -p %buildroot/var/log/postgres

mkdir -p %buildroot%logrotatedir
cat > %buildroot%logrotatedir/%{bname} <<EOF
/var/log/postgres/postgresql {
    notifempty
    missingok
    copytruncate
}
EOF

install -D -m755 %{SOURCE11} $RPM_BUILD_ROOT%{_initrddir}/postgresql

mv $RPM_BUILD_ROOT%{_docdir}/%{bname}/html $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}

%find_lang libpq
%find_lang libecpg
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata
%find_lang pgscripts
%find_lang initdb
%find_lang pg_config
%find_lang pg_ctl

cat pg_ctl.lang initdb.lang pg_config.lang psql.lang pg_dump.lang pgscripts.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst
# 20021226 warly waiting to be able to add a major in po name
cat libpq.lang libecpg.lang >> main.lst

# taken directly in build dir.
rm -fr $RPM_BUILD_ROOT%{_datadir}/doc/postgresql/contrib/

(
cd postgresql-mdk
make install DESTDIR=%buildroot
)
mkdir -p %buildroot%_sysconfdir/sysconfig
cat > %buildroot%_sysconfdir/sysconfig/mdkpg <<EOF
# Olivier Thauvin <nanardon@mandriva.org>

# This file control the behaviour of automatic
# Postgresql database migration between major version

# The directory where backups are stored
# BACKUPDIR=%pgdata/backups

# Deny to rpm to automatically migrate data
# Set to 1 to deny
# NORPMMIGRATION=0
EOF

mkdir -p %buildroot/%_sys_macros_dir
cat > %buildroot/%_sys_macros_dir/%{name}.macros <<EOF
%%postgresql_version %{version}
%%postgresql_major   %{current_major_version}
%%postgresql_minor   %{current_minor_version}
%%pgmodules_req Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
EOF

cat %{SOURCE13} > postgresql.mdv.releasenote
cat > README.urpmi <<EOF
You just installed or update %{bname} server.
You can found important informations about mandriva %{bname} rpms and database
management in:

%{_defaultdocdir}/%{name}-server-%{version}/postgresql.mdv.releasenote

Please, read it.
EOF

# postgres' .bash_profile
cat > $RPM_BUILD_ROOT/var/lib/pgsql/.bashrc <<EOF
# Default database location
# Olivier Thauvin <nanardon@mandriva.org>
PGDATA=%pgdata

# Setting up minimal envirronement
[ -f /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n
[ -f /etc/sysconfig/postgresql ] && . /etc/sysconfig/postgresql

export LANG LC_ALL LC_CTYPE LC_COLLATE LC_NUMERIC LC_CTYPE LC_TIME
export PGDATA
PS1="[\u@\h \W]\\$ "
EOF

%pre server
%_pre_useradd postgres /var/lib/pgsql /bin/bash

[ -f %_sysconfdir/sysconfig/mdkpg ] && . %_sysconfdir/sysconfig/mdkpg

[ "$NORPMMIGRATION" = 1 ] && exit 0
[ ! -f %pgdata/data/PG_VERSION ] && exit 0
[ `cat %pgdata/data/PG_VERSION` = %{current_major_version} ] && exit 0

%_bindir/mdk_pg -b -i %{version}-%{release}

%_bindir/mdk_pg -m -i %{version}-%{release}

%post server
/sbin/ldconfig

%posttrans server

[ -f %_sysconfdir/sysconfig/mdkpg ] && . %_sysconfdir/sysconfig/mdkpg

[ "$NORPMMIGRATION" = 1 ] && exit 0
[ -f ${BACKUPDIR}/db.%{version}-%{release}.gz ] || exit 0

service postgresql start

%_bindir/mdk_pg -r -i %{version}-%{release}

%_post_service %{name}

%preun server
%_preun_service %{name}

%postun server
/sbin/ldconfig
%_postun_userdel postgres

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libecpg} -p /sbin/ldconfig
%postun -n %{libecpg} -p /sbin/ldconfig

%clean
[ $RPM_BUILD_ROOT != '/' ] && rm -rf $RPM_BUILD_ROOT

%files -f main.lst 
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man7/*
%{_bindir}/mdk_pg
%config(noreplace) %_sysconfdir/sysconfig/mdkpg
%_sys_macros_dir/%{name}.macros

%if %produce_client
%files -n %{bname}
%endif

%files -n %{libname} 
%defattr(-,root,root)
%{_libdir}/libpq.so.%{major}*

%files -n %{libnamedevel}
%defattr(-,root,root)
%{_libdir}/libpq.so

%files -n %{libecpg}
%defattr(-,root,root)
%{_libdir}/libecpg.so.%{major_ecpg}*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*

%files -n %{libecpgdevel}
%defattr(-,root,root)
%{_libdir}/libecpg.so

%files docs
%defattr(-,root,root)
%doc %{_docdir}/%{name}-docs-%{version}

%files contrib
%defattr(-,root,root)
%doc contrib/*/README.* contrib/spi/*.example
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/chkpass.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch2.so
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/pg_buffercache.so
%{_libdir}/pgsql/adminpack.so
%{_libdir}/pgsql/hstore.so
%{_libdir}/pgsql/isn.so
%{_libdir}/pgsql/pg_freespacemap.so
%{_libdir}/pgsql/pgrowlocks.so
%{_libdir}/pgsql/sslinfo.so

%{_datadir}/pgsql/contrib/
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo

%files server -f server.lst
%defattr(-,root,root)
%config(noreplace) %{_initrddir}/postgresql
%doc README.urpmi postgresql.mdv.releasenote
%{_bindir}/initdb
%{_bindir}/ipcclean
%{_bindir}/pg_controldata 
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/ipcclean.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/*.sample
%{_datadir}/pgsql/timezone
%{_datadir}/pgsql/system_views.sql
%dir %{_libdir}/pgsql
%dir %{_datadir}/pgsql
%attr(644,postgres,postgres) %config(noreplace) %{_localstatedir}/pgsql/.bashrc
%attr(700,postgres,postgres) %dir %{pgdata}
%attr(-,postgres,postgres) %{pgdata}/data
%attr(700,postgres,postgres) %dir %{pgdata}/backups
%{_libdir}/pgsql/*_and_*.so
%{_datadir}/pgsql/conversion_create.sql
%{_datadir}/pgsql/information_schema.sql
%{_datadir}/pgsql/sql_features.txt

%{_datadir}/pgsql/postgres.shdescription
%dir %{_datadir}/pgsql/timezonesets
%{_datadir}/pgsql/timezonesets/Africa.txt
%{_datadir}/pgsql/timezonesets/America.txt
%{_datadir}/pgsql/timezonesets/Antarctica.txt
%{_datadir}/pgsql/timezonesets/Asia.txt
%{_datadir}/pgsql/timezonesets/Atlantic.txt
%{_datadir}/pgsql/timezonesets/Australia
%{_datadir}/pgsql/timezonesets/Australia.txt
%{_datadir}/pgsql/timezonesets/Default
%{_datadir}/pgsql/timezonesets/Etc.txt
%{_datadir}/pgsql/timezonesets/Europe.txt
%{_datadir}/pgsql/timezonesets/India
%{_datadir}/pgsql/timezonesets/Indian.txt
%{_datadir}/pgsql/timezonesets/Pacific.txt

%attr(700,postgres,postgres) %dir /var/log/postgres
%logrotatedir/%{bname}

%files devel
%defattr(-,root,root)
%doc doc/TODO doc/TODO.detail
%{_includedir}/pgsql
%{_bindir}/ecpg
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pgsql/pgxs/
%{_mandir}/man1/ecpg.1*
%{_bindir}/pg_config
%{_mandir}/man1/pg_config.1*

%if %produce_devel
%files -n %{bname}-devel
%endif

%files pl 
%defattr(-,root,root) 

%files plpython
%defattr(-,root,root) 
%{_libdir}/pgsql/plpython.so 

%files plperl
%defattr(-,root,root) 
%{_libdir}/pgsql/plperl.so 

%files pltcl
%defattr(-,root,root) 
%{_libdir}/pgsql/pltcl.so 
%{_bindir}/pltcl_delmod 
%{_bindir}/pltcl_listmod 
%{_bindir}/pltcl_loadmod 
%{_datadir}/pgsql/unknown.pltcl 

%files plpgsql
%defattr(-,root,root) 
%{_libdir}/pgsql/plpgsql.so

%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{_libdir}/pgsql/test/*
%attr(-,postgres,postgres) %dir %{_libdir}/pgsql/test
