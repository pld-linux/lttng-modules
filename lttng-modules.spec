#
# Conditional build:
%bcond_without	allprobes	# all probes build (some probes, e.g. fs, need full kernel source)
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	1
%define		pname	lttng-modules
Summary:	LTTng 2.x kernel modules
Summary(pl.UTF-8):	Moduły jądra LTTng 2.x
Name:		%{pname}%{_alt_kernel}
Version:	2.5.2
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://lttng.org/files/lttng-modules/%{pname}-%{version}.tar.bz2
# Source0-md5:	74d2fd161fdbf3426c6af5a36a774d4a
Patch0:		build.patch
Patch1:		linux-3.17.patch
Patch2:		linux-3.18.patch
URL:		http://lttng.org/
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.38}
%{?with_allprobes:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-source >= 3:2.6.38}}
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LTTng 2.x kernel modules.

%description -l pl.UTF-8
Moduły jądra LTTng 2.x.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-lttng\
Summary:	LTTng 2.x modules for Linux kernel\
Summary(pl.UTF-8):	Moduły LTTng 2.x dla jądra Linuksa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-lttng\
LTTng 2.x modules for Linux kernel.\
\
%description -n kernel%{_alt_kernel}-lttng -l pl.UTF-8\
Moduły LTTng 2.x dla jądra Linuksa.\
\
%files -n kernel%{_alt_kernel}-lttng\
%defattr(644,root,root,755)\
%doc ChangeLog LICENSE README TODO\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-ring-buffer-*.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-statedump.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-tracer.ko*\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng/lib\
/lib/modules/%{_kernel_ver}/kernel/lttng/lib/lttng-lib-ring-buffer.ko*\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng/probes\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-ftrace.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-kprobes.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-kretprobes.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-probe-*.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-types.ko*\
\
%post	-n kernel%{_alt_kernel}-lttng\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-lttng\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%{__make} \\\
	KERNELDIR=%{_kernelsrcdir} \\\
	EXTCFLAGS="%{rpmcflags}"\
p=`pwd`\
%{__make} modules_install \\\
	INSTALL_MOD_PATH=$p/installed \\\
	INSTALL_MOD_DIR=kernel/lttng \\\
	KERNELDIR=%{_kernelsrcdir}\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
