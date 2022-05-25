#
# Conditional build:
%bcond_without	kernelsrc	# probes which require full kernel source (kvm, btrfs, ext4, regmap)
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	2
%define		pname	lttng-modules
Summary:	LTTng 2.x kernel modules
Summary(pl.UTF-8):	Moduły jądra LTTng 2.x
Name:		%{pname}%{_alt_kernel}
Version:	2.13.3
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	https://lttng.org/files/lttng-modules/%{pname}-%{version}.tar.bz2
# Source0-md5:	7f25ed040ca46c3c643e9a44dd258d3b
Patch0:		build.patch
Patch1:		0001-Fix-compaction-migratepages-event-name.patch
Patch2:		0002-Fix-tracepoint-event-allow-same-provider-and-event-n.patch
Patch3:		0003-fix-sched-tracing-Don-t-re-read-p-state-when-emittin.patch
Patch4:		0004-fix-block-remove-genhd.h-v5.18.patch
Patch5:		0005-fix-scsi-block-Remove-REQ_OP_WRITE_SAME-support-v5.1.patch
Patch6:		0006-fix-random-remove-unused-tracepoints-v5.18.patch
Patch7:		0007-fix-kprobes-Use-rethook-for-kretprobe-if-possible-v5.patch
Patch8:		0008-fix-scsi-core-Remove-scsi-scsi_request.h-v5.18.patch
Patch9:		0009-Rename-genhd-wrapper-to-blkdev.patch
Patch10:	0010-fix-mm-compaction-cleanup-the-compaction-trace-event.patch
Patch11:	0011-Fix-do-not-warn-on-unknown-counter-ioctl.patch
Patch12:	0012-fix-KVM-x86-Unexport-kvm_x86_ops-v5.18.patch
Patch13:	0013-fix-sched-tracing-Append-prev_state-to-tp-args-inste.patch
URL:		https://lttng.org/
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:3.0}
%{?with_kernelsrc:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-source >= 3:3.0}}
BuildRequires:	rpmbuild(macros) >= 1.746
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
%doc %{pname}-%{version}/{ChangeLog,LICENSE,README.md}\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-clock.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-counter-client-percpu-32-modular.ko.*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-counter-client-percpu-64-modular.ko.*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-ring-buffer-*.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-statedump.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-tracer.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lttng-wrapper.ko*\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng/lib\
/lib/modules/%{_kernel_ver}/kernel/lttng/lib/lttng-counter.ko.*\
/lib/modules/%{_kernel_ver}/kernel/lttng/lib/lttng-lib-ring-buffer.ko*\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng/probes\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-kprobes.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-kretprobes.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-probe-*.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/probes/lttng-uprobes.ko*\
%dir /lib/modules/%{_kernel_ver}/kernel/lttng/tests\
/lib/modules/%{_kernel_ver}/kernel/lttng/tests/lttng-clock-plugin-test.ko*\
/lib/modules/%{_kernel_ver}/kernel/lttng/tests/lttng-test.ko*\
\
%post	-n kernel%{_alt_kernel}-lttng\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-lttng\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%{__make} clean \\\
	KERNELDIR=%{_kernelsrcdir}\
%{__make} \\\
	KERNELDIR=%{_kernelsrcdir}\
p=`pwd`\
%{__make} modules_install \\\
	INSTALL_MOD_PATH=$p/../installed \\\
	INSTALL_MOD_DIR=kernel/lttng \\\
	KERNELDIR=%{_kernelsrcdir}\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -qc -n %{name}-%{version}
cd %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
cd  %{pname}-%{version}
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
