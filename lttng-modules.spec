#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	allprobes	# all probes build (some probes, e.g. fs, need full kernel source)
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	1
%define		pname	lttng-modules
Summary:	LTTng 2.x kernel modules
Summary(pl.UTF-8):	Moduły jądra LTTng 2.x
Name:		%{pname}%{_alt_kernel}
Version:	2.3.4
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://lttng.org/files/lttng-modules/%{pname}-%{version}.tar.bz2
# Source0-md5:	6941d6c2b149d9b301e388a9b4a99470
Patch0:		%{name}-linux-3.13.patch
URL:		http://lttng.org/
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.38
%{?with_allprobes:BuildRequires:	kernel%{_alt_kernel}-source >= 3:2.6.38}
%endif
BuildRequires:	rpmbuild(macros) >= 1.678
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
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
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

%{expand:%kpkg}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%build
%{expand:%bkpkg}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
